# Flowdex Streaming Pipeline (Phase 2)

Bu klasör, Faz 2 kapsamında geliştirilen gerçek zamanlı veri hattının referans
uygulamalarını içerir:

- `mock_price_producer.py` → Kafka'ya sentetik fiyat tikleri üretir.
- `spark_ohlcv_job.py` → PySpark Structured Streaming ile tik verisini OHLCV
  mumlarına dönüştürerek PostgreSQL tablolarına yazar.

## 1. Hazırlık

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Kafka topiğini oluştur (tek seferlik)
./scripts/create_topics.sh
```

## 2. Sentetik veri üreticisi

```bash
python streaming/mock_price_producer.py \
  --brokers localhost:9092 \
  --topic prices.ticks \
  --symbols BTC ETH SOL AVAX \
  --interval 0.5 \
  --verbose
```

Komut her yarım saniyede seçilen semboller için rastgele tikler üretir. ENV ile
`KAFKA_BROKERS`, `KAFKA_TOPIC` ve `PRODUCER_INTERVAL` değişkenleri de
özelleştirilebilir.

## 3. PySpark OHLCV job’ı

```bash
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.postgresql:postgresql:42.7.3 \
  streaming/spark_ohlcv_job.py
```

İsteğe bağlı ortam değişkenleri:

- `DATABASE_URL` veya `MARKET_DATABASE_URL` → PostgreSQL bağlantısı.
- `BAR_INTERVAL` / `BAR_INTERVAL_LABEL` → pencere boyutu ve etiket.
- `CHECKPOINT_DIR` → Spark checkpoint dizini.

Job, Kafka’dan gelen tikleri 1 dakikalık pencereler halinde agregat edip
`market_ohlcv` tablosuna yazar ve `market_price_snapshots` tablosunu günceller.
Backend API aynı tabloları okuyarak canlı dashboard’a hizmet eder.

> Not: Demo amaçlı metrikler (market cap, yüzde değişim, hacim) basitleştirilmiş
> formüllerle hesaplanır. Gerçek üretim senaryosunda finansal kurallara uygun
> daha gelişmiş türevler uygulanmalıdır.
