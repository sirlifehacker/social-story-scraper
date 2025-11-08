"""Settings and API key management routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..models.user import User
from ..models.api_key import APIKey, ServiceName
from ..models.user_preferences import UserPreferences
from ..schemas.api_key import APIKeyCreate, APIKeyUpdate, APIKeyResponse
from ..schemas.preferences import UserPreferencesUpdate, UserPreferencesResponse
from ..core.deps import get_current_active_user
from ..core.security import encrypt_api_key, decrypt_api_key

router = APIRouter(prefix="/settings", tags=["Settings"])


# API Keys Management
@router.get("/api-keys", response_model=List[APIKeyResponse])
async def get_api_keys(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all API keys for current user (encrypted values not returned)"""
    api_keys = db.query(APIKey).filter(APIKey.user_id == current_user.id).all()
    return api_keys


@router.post("/api-keys", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    api_key_data: APIKeyCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create or update API key for a service"""
    # Check if API key for this service already exists
    existing_key = db.query(APIKey).filter(
        APIKey.user_id == current_user.id,
        APIKey.service_name == api_key_data.service_name
    ).first()

    if existing_key:
        # Update existing key
        existing_key.encrypted_key = encrypt_api_key(api_key_data.api_key)
        existing_key.is_active = True
        db.commit()
        db.refresh(existing_key)
        return existing_key
    else:
        # Create new key
        encrypted_key = encrypt_api_key(api_key_data.api_key)
        new_api_key = APIKey(
            user_id=current_user.id,
            service_name=api_key_data.service_name,
            encrypted_key=encrypted_key
        )
        db.add(new_api_key)
        db.commit()
        db.refresh(new_api_key)
        return new_api_key


@router.put("/api-keys/{service_name}", response_model=APIKeyResponse)
async def update_api_key(
    service_name: ServiceName,
    api_key_data: APIKeyUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update API key for a specific service"""
    api_key = db.query(APIKey).filter(
        APIKey.user_id == current_user.id,
        APIKey.service_name == service_name
    ).first()

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"API key for {service_name} not found"
        )

    api_key.encrypted_key = encrypt_api_key(api_key_data.api_key)
    api_key.is_active = api_key_data.is_active
    db.commit()
    db.refresh(api_key)
    return api_key


@router.delete("/api-keys/{service_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    service_name: ServiceName,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete API key for a specific service"""
    api_key = db.query(APIKey).filter(
        APIKey.user_id == current_user.id,
        APIKey.service_name == service_name
    ).first()

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"API key for {service_name} not found"
        )

    db.delete(api_key)
    db.commit()
    return None


# User Preferences Management
@router.get("/preferences", response_model=UserPreferencesResponse)
async def get_preferences(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user preferences"""
    preferences = db.query(UserPreferences).filter(
        UserPreferences.user_id == current_user.id
    ).first()

    if not preferences:
        # Create default preferences if they don't exist
        preferences = UserPreferences(user_id=current_user.id)
        db.add(preferences)
        db.commit()
        db.refresh(preferences)

    return preferences


@router.put("/preferences", response_model=UserPreferencesResponse)
async def update_preferences(
    preferences_data: UserPreferencesUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user preferences"""
    preferences = db.query(UserPreferences).filter(
        UserPreferences.user_id == current_user.id
    ).first()

    if not preferences:
        preferences = UserPreferences(user_id=current_user.id)
        db.add(preferences)

    # Update only provided fields
    update_data = preferences_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(preferences, field, value)

    db.commit()
    db.refresh(preferences)
    return preferences
