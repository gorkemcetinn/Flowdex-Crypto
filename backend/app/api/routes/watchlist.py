"""Watchlist endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...models.user import User
from ...models.watchlist_item import WatchlistItem
from ...schemas.watchlist import WatchlistItemCreate, WatchlistItemRead
from ..deps import get_db

router = APIRouter()


def _ensure_user_exists(user_id: str, db: Session) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/{user_id}", response_model=list[WatchlistItemRead])
def read_watchlist(user_id: str, db: Session = Depends(get_db)) -> list[WatchlistItem]:
    """Return the watchlist entries belonging to a user."""

    _ensure_user_exists(user_id, db)
    result = db.execute(
        select(WatchlistItem).where(WatchlistItem.user_id == user_id).order_by(WatchlistItem.created_at.desc())
    )
    return list(result.scalars().all())


@router.post("/{user_id}", response_model=WatchlistItemRead, status_code=status.HTTP_201_CREATED)
def add_watchlist_item(
    user_id: str,
    payload: WatchlistItemCreate,
    response: Response,
    db: Session = Depends(get_db),
) -> WatchlistItem:
    """Add a symbol to the user's watchlist."""

    _ensure_user_exists(user_id, db)
    normalized_symbol = payload.symbol.upper()

    existing_item = db.execute(
        select(WatchlistItem).where(
            WatchlistItem.user_id == user_id, WatchlistItem.symbol == normalized_symbol
        )
    ).scalar_one_or_none()
    if existing_item:
        response.status_code = status.HTTP_200_OK
        return existing_item

    item = WatchlistItem(user_id=user_id, symbol=normalized_symbol)
    db.add(item)
    db.commit()
    db.refresh(item)
    response.status_code = status.HTTP_201_CREATED
    return item


@router.delete("/{user_id}/{symbol}", status_code=status.HTTP_204_NO_CONTENT)
def remove_watchlist_item(user_id: str, symbol: str, db: Session = Depends(get_db)) -> Response:
    """Remove a symbol from the user's watchlist."""

    _ensure_user_exists(user_id, db)
    normalized_symbol = symbol.upper()

    item = db.execute(
        select(WatchlistItem).where(
            WatchlistItem.user_id == user_id, WatchlistItem.symbol == normalized_symbol
        )
    ).scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Watchlist item not found")

    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
