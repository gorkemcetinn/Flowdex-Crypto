"""User related API endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...models.user import User
from ...models.user_settings import UserSettings
from ...schemas.user import UserCreate, UserRead
from ..deps import get_db

router = APIRouter()


def _normalize_email(value: EmailStr) -> str:
    """Return a lowercase string representation of the email."""

    return str(value).lower()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    response: Response,
    db: Session = Depends(get_db),
) -> User:
    """Create a new user or return the existing record."""

    normalized_email = _normalize_email(payload.email)
    existing_user = db.execute(select(User).where(User.email == normalized_email)).scalar_one_or_none()
    if existing_user:
        response.status_code = status.HTTP_200_OK
        return existing_user

    user = User(email=normalized_email)
    db.add(user)
    db.flush()

    db.add(UserSettings(user_id=user.id))
    db.commit()
    db.refresh(user)
    response.status_code = status.HTTP_201_CREATED
    return user


@router.get("/by-email", response_model=UserRead)
def read_user_by_email(email: EmailStr, db: Session = Depends(get_db)) -> User:
    """Return a user by their email address."""

    normalized_email = _normalize_email(email)
    user = db.execute(select(User).where(User.email == normalized_email)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: str, db: Session = Depends(get_db)) -> User:
    """Fetch a single user by identifier."""

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
