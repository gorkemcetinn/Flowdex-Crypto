"""Pydantic schemas for watchlist resources."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WatchlistItemBase(BaseModel):
    """Base schema containing shared watchlist fields."""

    symbol: str = Field(..., min_length=1, max_length=20)


class WatchlistItemCreate(WatchlistItemBase):
    """Payload schema for watchlist creation."""

    pass


class WatchlistItemRead(WatchlistItemBase):
    """Schema for returning watchlist entries."""

    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
