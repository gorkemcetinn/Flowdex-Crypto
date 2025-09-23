"""Ensure all models are imported for SQLAlchemy metadata."""
from __future__ import annotations

from .base_class import Base  # noqa: F401
from ..models import user, user_settings, watchlist_item  # noqa: F401
