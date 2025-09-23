"""Pydantic schemas for user resources."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: EmailStr


class UserRead(BaseModel):
    """Schema for reading user information."""

    id: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
