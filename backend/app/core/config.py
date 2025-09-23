"""Application configuration settings."""
from __future__ import annotations

import os
from functools import lru_cache


class Settings:
    """Configuration values loaded from environment variables."""

    api_v1_prefix: str = "/api"
    project_name: str = "Flowdex Crypto API"

    def __init__(self) -> None:
        self.database_url: str = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://flowdex:flowdex@localhost:5432/flowdex",
        )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""

    return Settings()


settings = get_settings()
