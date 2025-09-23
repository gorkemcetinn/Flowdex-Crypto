"""Market data endpoints powering the Phase 1 UI."""
from __future__ import annotations

import json
from typing import AsyncIterator, Iterable

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...models.user import User
from ...models.watchlist_item import WatchlistItem
from ...schemas.market import MarketAssetBase, MarketAssetDetail, TopMoversResponse, WatchlistAsset
from ...services import market_data
from ..deps import get_db

router = APIRouter()


def _ensure_user(user_id: str, db: Session) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def _extract_symbols(result: Iterable[WatchlistItem]) -> list[str]:
    return [item.symbol for item in result]


@router.get("/overview", response_model=list[MarketAssetBase])
def market_overview(
    limit: int = Query(8, ge=1, le=20), db: Session = Depends(get_db)
) -> list[dict]:
    """Return the top assets ranked by market cap."""

    return market_data.get_overview(limit, db=db)


@router.get("/top-movers", response_model=TopMoversResponse)
def top_movers(
    limit: int = Query(4, ge=1, le=6), db: Session = Depends(get_db)
) -> TopMoversResponse:
    """Return the leading gainers and laggards for the session."""

    payload = market_data.get_top_movers(limit, db=db)
    return TopMoversResponse(**payload)


@router.get("/watchlist/{user_id}", response_model=list[WatchlistAsset])
def watchlist_with_quotes(user_id: str, db: Session = Depends(get_db)) -> list[dict]:
    """Augment the user's watchlist with the latest quote snapshot."""

    _ensure_user(user_id, db)
    result = db.execute(
        select(WatchlistItem)
        .where(WatchlistItem.user_id == user_id)
        .order_by(WatchlistItem.created_at.asc())
    )
    items = result.scalars().all()
    symbols = _extract_symbols(items)
    if not symbols:
        return []
    return market_data.get_watchlist_snapshots(symbols, db=db)


@router.get("/stream")
async def stream_watchlist(
    symbols: str = Query(..., min_length=1),
    max_events: int = Query(5, ge=1, le=20),
    delay: float = Query(0.05, ge=0.01, le=1.0),
    db: Session = Depends(get_db),
) -> StreamingResponse:
    """Provide a short-lived SSE stream of watchlist quotes."""

    requested = [symbol.strip().upper() for symbol in symbols.split(",") if symbol.strip()]
    unique_symbols = []
    for symbol in requested:
        if symbol not in unique_symbols and market_data.available_symbol(symbol, db=db):
            unique_symbols.append(symbol)

    if not unique_symbols:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No supported symbols provided")

    baseline = market_data.get_watchlist_snapshots(unique_symbols, db=db)
    if not baseline:
        baseline = market_data.get_watchlist_snapshots(unique_symbols)

    async def event_generator() -> AsyncIterator[str]:
        async for event in market_data.stream_quotes(
            unique_symbols,
            iterations=max_events,
            delay=delay,
            seed_quotes=baseline,
        ):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/{symbol}", response_model=MarketAssetDetail)
def market_detail(symbol: str, db: Session = Depends(get_db)) -> dict:
    """Return detail for an individual asset."""

    asset = market_data.get_asset_detail(symbol, db=db)
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Symbol not supported")
    return asset
