"""PySpark streaming job that aggregates tick data into OHLCV candles."""
from __future__ import annotations

import os
from typing import List

from pyspark.sql import DataFrame, SparkSession, functions as F, types as T
from sqlalchemy import Column, DateTime, Float, JSON, MetaData, String, Table, create_engine, select
from sqlalchemy.dialects.postgresql import insert as pg_insert

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BROKERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "prices.ticks")
INTERVAL = os.getenv("BAR_INTERVAL", "1 minute")
INTERVAL_LABEL = os.getenv("BAR_INTERVAL_LABEL", "1m")

DATABASE_URL = os.getenv(
    "MARKET_DATABASE_URL",
    os.getenv("DATABASE_URL", "postgresql+psycopg2://flowdex:flowdex@localhost:5432/flowdex"),
)

ENGINE = create_engine(DATABASE_URL)

METADATA = MetaData()

PRICE_TABLE = Table(
    "market_price_snapshots",
    METADATA,
    Column("symbol", String(16), primary_key=True),
    Column("name", String(128)),
    Column("price", Float),
    Column("percent_change_24h", Float),
    Column("percent_change_7d", Float),
    Column("volume_24h", Float),
    Column("market_cap", Float),
    Column("sparkline", JSON),
    Column("high_24h", Float),
    Column("low_24h", Float),
    Column("description", String(256)),
)

OHLCV_TABLE = Table(
    "market_ohlcv",
    METADATA,
    Column("symbol", String(16), primary_key=True),
    Column("interval", String(8), primary_key=True),
    Column("bucket_start", DateTime(timezone=True), primary_key=True),
    Column("open", Float),
    Column("high", Float),
    Column("low", Float),
    Column("close", Float),
    Column("volume", Float),
)


TICK_SCHEMA = T.StructType(
    [
        T.StructField("symbol", T.StringType(), nullable=False),
        T.StructField("price", T.DoubleType(), nullable=False),
        T.StructField("volume", T.DoubleType(), nullable=False),
        T.StructField("timestamp", T.StringType(), nullable=False),
        T.StructField("source", T.StringType(), nullable=True),
    ]
)


def ensure_minimum_sparkline(values: List[float]) -> List[float]:
    if not values:
        return [0.0, 0.0]
    if len(values) == 1:
        return [values[0], values[0]]
    return values


def upsert_batch(batch_df: DataFrame, batch_id: int) -> None:
    if batch_df.rdd.isEmpty():
        return

    enriched = (
        batch_df.withColumn("bucket_start", F.col("window").getField("start"))
        .withColumn("bucket_end", F.col("window").getField("end"))
        .drop("window")
    )

    records = [
        {
            "symbol": row.symbol,
            "interval": INTERVAL_LABEL,
            "bucket_start": row.bucket_start,
            "open": float(row.open),
            "high": float(row.high),
            "low": float(row.low),
            "close": float(row.close),
            "volume": float(row.volume),
        }
        for row in enriched.toLocalIterator()
    ]

    if not records:
        return

    with ENGINE.begin() as connection:
        ohlcv_stmt = pg_insert(OHLCV_TABLE).values(records)
        update_columns = {
            "open": ohlcv_stmt.excluded.open,
            "high": ohlcv_stmt.excluded.high,
            "low": ohlcv_stmt.excluded.low,
            "close": ohlcv_stmt.excluded.close,
            "volume": ohlcv_stmt.excluded.volume,
        }
        connection.execute(
            ohlcv_stmt.on_conflict_do_update(
                index_elements=[
                    OHLCV_TABLE.c.symbol,
                    OHLCV_TABLE.c.interval,
                    OHLCV_TABLE.c.bucket_start,
                ],
                set_=update_columns,
            )
        )

        symbols = [record["symbol"] for record in records]
        existing_rows = {
            row.symbol: row
            for row in connection.execute(
                select(PRICE_TABLE).where(PRICE_TABLE.c.symbol.in_(symbols))
            )
        }

        for record in records:
            previous = existing_rows.get(record["symbol"])
            sparkline = []
            if previous and previous.sparkline:
                sparkline = list(previous.sparkline)
            sparkline.append(record["close"])
            sparkline = ensure_minimum_sparkline(sparkline[-12:])
            baseline = sparkline[0] if sparkline else record["close"]
            percent_change = 0.0
            if baseline:
                percent_change = round(((sparkline[-1] - baseline) / baseline) * 100, 4)
            volume_24h = record["volume"]
            if previous and previous.volume_24h:
                volume_24h = round(float(previous.volume_24h) * 0.75 + record["volume"], 4)

            payload = {
                "symbol": record["symbol"],
                "name": f"{record['symbol']} Spot",
                "price": record["close"],
                "percent_change_24h": percent_change,
                "percent_change_7d": percent_change,
                "volume_24h": volume_24h,
                "market_cap": round(record["close"] * 1_000_000, 2),
                "sparkline": sparkline,
                "high_24h": max(sparkline),
                "low_24h": min(sparkline),
                "description": f"Streaming market data for {record['symbol']}",
            }

            price_stmt = pg_insert(PRICE_TABLE).values(payload)
            connection.execute(
                price_stmt.on_conflict_do_update(
                    index_elements=[PRICE_TABLE.c.symbol],
                    set_={
                        "name": price_stmt.excluded.name,
                        "price": price_stmt.excluded.price,
                        "percent_change_24h": price_stmt.excluded.percent_change_24h,
                        "percent_change_7d": price_stmt.excluded.percent_change_7d,
                        "volume_24h": price_stmt.excluded.volume_24h,
                        "market_cap": price_stmt.excluded.market_cap,
                        "sparkline": price_stmt.excluded.sparkline,
                        "high_24h": price_stmt.excluded.high_24h,
                        "low_24h": price_stmt.excluded.low_24h,
                        "description": price_stmt.excluded.description,
                    },
                )
            )


def build_stream() -> None:
    spark = (
        SparkSession.builder.appName("flowdex-ohlcv-stream")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    raw = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
        .option("subscribe", KAFKA_TOPIC)
        .option("startingOffsets", "latest")
        .load()
    )

    parsed = (
        raw.selectExpr("CAST(value AS STRING) as json")
        .select(F.from_json(F.col("json"), TICK_SCHEMA).alias("tick"))
        .select("tick.*")
        .withColumn("event_time", F.to_timestamp("timestamp"))
        .dropna(subset=["event_time", "symbol"])
    )

    candles = (
        parsed.withWatermark("event_time", "2 minutes")
        .groupBy(
            "symbol",
            F.window("event_time", INTERVAL),
        )
        .agg(
            F.first("price").alias("open"),
            F.max("price").alias("high"),
            F.min("price").alias("low"),
            F.last("price").alias("close"),
            F.sum("volume").alias("volume"),
        )
    )

    query = (
        candles.writeStream.outputMode("update")
        .foreachBatch(upsert_batch)
        .option("checkpointLocation", os.getenv("CHECKPOINT_DIR", "/tmp/flowdex-checkpoints"))
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":  # pragma: no cover - entrypoint
    build_stream()
