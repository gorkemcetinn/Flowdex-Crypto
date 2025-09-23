"""Database engine and session handling utilities."""
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


def get_session():
    """Provide a transactional database session."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
