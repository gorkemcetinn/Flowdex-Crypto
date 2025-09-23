"""Integration tests for the Phase 0 FastAPI skeleton."""
from __future__ import annotations

from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.api.deps import get_db
from backend.app.db import session as db_session
from backend.app.db.base import Base
from backend.app.main import app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Provide a test client with an in-memory database."""

    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    TestingSessionLocal = sessionmaker(
        bind=engine, autocommit=False, autoflush=False, future=True
    )
    Base.metadata.create_all(bind=engine)

    original_engine = db_session.engine
    original_session_local = db_session.SessionLocal

    db_session.engine = engine
    db_session.SessionLocal = TestingSessionLocal

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.pop(get_db, None)
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

    db_session.engine = original_engine
    db_session.SessionLocal = original_session_local


def test_user_creation_and_lookup(client: TestClient) -> None:
    """Users can be created and fetched via API routes."""

    response = client.post("/api/users", json={"email": "alice@example.com"})
    assert response.status_code == 201
    user = response.json()
    assert user["email"] == "alice@example.com"

    user_id = user["id"]
    by_id = client.get(f"/api/users/{user_id}")
    assert by_id.status_code == 200
    assert by_id.json()["id"] == user_id

    by_email = client.get("/api/users/by-email", params={"email": "alice@example.com"})
    assert by_email.status_code == 200
    assert by_email.json()["id"] == user_id


def test_watchlist_crud(client: TestClient) -> None:
    """Watchlist endpoints support create/read/delete flows."""

    user = client.post("/api/users", json={"email": "bob@example.com"}).json()
    user_id = user["id"]

    add_resp = client.post(f"/api/watchlist/{user_id}", json={"symbol": "btc"})
    assert add_resp.status_code == 201
    watch_item = add_resp.json()
    assert watch_item["symbol"] == "BTC"

    list_resp = client.get(f"/api/watchlist/{user_id}")
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert len(items) == 1

    duplicate_resp = client.post(f"/api/watchlist/{user_id}", json={"symbol": "BTC"})
    assert duplicate_resp.status_code == 200
    assert duplicate_resp.json()["id"] == watch_item["id"]

    delete_resp = client.delete(f"/api/watchlist/{user_id}/btc")
    assert delete_resp.status_code == 204

    empty_resp = client.get(f"/api/watchlist/{user_id}")
    assert empty_resp.status_code == 200
    assert empty_resp.json() == []


def test_user_settings_defaults_and_update(client: TestClient) -> None:
    """Default settings are created and can be updated."""

    user = client.post("/api/users", json={"email": "carol@example.com"}).json()
    user_id = user["id"]

    initial = client.get(f"/api/settings/{user_id}")
    assert initial.status_code == 200
    settings = initial.json()
    assert settings["currency"] == "USD"
    assert settings["theme"] == "light"

    update = client.put(
        f"/api/settings/{user_id}",
        json={"currency": "eur", "theme": "DARK", "language": "TR"},
    )
    assert update.status_code == 200
    updated = update.json()
    assert updated["currency"] == "EUR"
    assert updated["theme"] == "dark"
    assert updated["language"] == "tr"
