"""User settings endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...models.user import User
from ...models.user_settings import UserSettings
from ...schemas.user_settings import UserSettingsRead, UserSettingsUpdate
from ..deps import get_db

router = APIRouter()


def _get_or_create_settings(user_id: str, db: Session) -> UserSettings:
    settings = db.get(UserSettings, user_id)
    if settings:
        return settings

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    settings = UserSettings(user_id=user_id)
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings


@router.get("/{user_id}", response_model=UserSettingsRead)
def read_settings(user_id: str, db: Session = Depends(get_db)) -> UserSettings:
    """Fetch the stored settings for a user, creating defaults if needed."""

    return _get_or_create_settings(user_id, db)


@router.put("/{user_id}", response_model=UserSettingsRead)
def update_settings(
    user_id: str,
    payload: UserSettingsUpdate,
    db: Session = Depends(get_db),
) -> UserSettings:
    """Update user settings with the provided payload."""

    settings = _get_or_create_settings(user_id, db)

    update_data = payload.model_dump(exclude_unset=True)
    if "currency" in update_data and update_data["currency"]:
        update_data["currency"] = update_data["currency"].upper()
    if "language" in update_data and update_data["language"]:
        update_data["language"] = update_data["language"].lower()
    if "theme" in update_data and update_data["theme"]:
        update_data["theme"] = update_data["theme"].lower()

    for field, value in update_data.items():
        setattr(settings, field, value)

    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings
