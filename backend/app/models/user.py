"""User model."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base_class import Base


class User(Base):
    """Represents an application user."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    watchlist_items: Mapped[List["WatchlistItem"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    settings: Mapped[Optional["UserSettings"]] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
