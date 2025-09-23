"""Database models that store market data derived from the streaming pipeline."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base_class import Base


class MarketPriceSnapshot(Base):
    """Latest quote snapshot for a tradeable asset."""

    __tablename__ = "market_price_snapshots"

    symbol: Mapped[str] = mapped_column(String(16), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    price: Mapped[float] = mapped_column(Float)
    percent_change_24h: Mapped[float] = mapped_column(Float)
    percent_change_7d: Mapped[float] = mapped_column(Float, default=0)
    volume_24h: Mapped[float] = mapped_column(Float)
    market_cap: Mapped[float] = mapped_column(Float)
    sparkline: Mapped[list[float]] = mapped_column(JSON, default=list)
    high_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    low_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class MarketOhlcv(Base):
    """Aggregated OHLCV candle produced by the Spark streaming job."""

    __tablename__ = "market_ohlcv"

    symbol: Mapped[str] = mapped_column(String(16), primary_key=True)
    interval: Mapped[str] = mapped_column(String(8), primary_key=True)
    bucket_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    open: Mapped[float] = mapped_column(Float)
    high: Mapped[float] = mapped_column(Float)
    low: Mapped[float] = mapped_column(Float)
    close: Mapped[float] = mapped_column(Float)
    volume: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
