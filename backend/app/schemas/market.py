"""Pydantic schemas for market-focused endpoints."""
from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field


class MarketAssetBase(BaseModel):
    """Common fields shared by market assets."""

    model_config = ConfigDict(from_attributes=True)

    symbol: str
    name: str
    price: float = Field(..., ge=0)
    percent_change_24h: float
    percent_change_7d: float
    volume_24h: float = Field(..., ge=0)
    market_cap: float = Field(..., ge=0)
    sparkline: List[float] = Field(..., min_length=2)


class MarketAssetDetail(MarketAssetBase):
    """Extended information for a specific asset."""

    high_24h: float
    low_24h: float
    description: str


class MarketMove(BaseModel):
    """Represents a top mover entry."""

    symbol: str
    name: str
    price: float = Field(..., ge=0)
    percent_change_24h: float
    volume_24h: float = Field(..., ge=0)


class TopMoversResponse(BaseModel):
    """Payload containing gainers and losers lists."""

    gainers: List[MarketMove]
    losers: List[MarketMove]


class WatchlistAsset(MarketAssetBase):
    """Watchlist snapshot shares the overview fields."""

    pass
