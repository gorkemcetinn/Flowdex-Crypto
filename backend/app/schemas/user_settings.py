"""Pydantic schemas for user settings resources."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserSettingsUpdate(BaseModel):
    """Schema for updating user preferences."""

    currency: Optional[str] = Field(default=None, min_length=1, max_length=8)
    theme: Optional[str] = Field(default=None, min_length=1, max_length=32)
    language: Optional[str] = Field(default=None, min_length=2, max_length=8)


class UserSettingsRead(BaseModel):
    """Schema for returning stored user settings."""

    user_id: str
    currency: str
    theme: str
    language: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
