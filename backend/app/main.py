"""FastAPI application entrypoint."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import markets, user_settings, users, watchlist
from .core.config import settings
from .db import session as db_session
from .db.base import Base


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=db_session.engine)
    yield


app = FastAPI(title=settings.project_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    """Simple health-check endpoint for infrastructure probes."""

    return {"status": "ok"}


app.include_router(users.router, prefix=f"{settings.api_v1_prefix}/users", tags=["users"])
app.include_router(
    watchlist.router, prefix=f"{settings.api_v1_prefix}/watchlist", tags=["watchlist"]
)
app.include_router(
    markets.router, prefix=f"{settings.api_v1_prefix}/markets", tags=["markets"]
)
app.include_router(
    user_settings.router,
    prefix=f"{settings.api_v1_prefix}/settings",
    tags=["settings"],
)
