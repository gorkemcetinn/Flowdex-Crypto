"""User settings model."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base_class import Base


class UserSettings(Base):
    """Stores user preferences such as theme or currency."""

    __tablename__ = "user_settings"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    currency: Mapped[str] = mapped_column(String(8), default="USD", nullable=False)
    theme: Mapped[str] = mapped_column(String(32), default="light", nullable=False)
    language: Mapped[str] = mapped_column(String(8), default="en", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="settings")
