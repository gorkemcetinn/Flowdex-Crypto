"""FastAPI dependencies shared across routers."""
from __future__ import annotations

from sqlalchemy.orm import Session

from ..db.session import get_session


def get_db() -> Session:
    """Provide a scoped SQLAlchemy session."""

    yield from get_session()
