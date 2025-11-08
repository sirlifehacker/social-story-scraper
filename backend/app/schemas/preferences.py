"""User Preferences schemas"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, time
from typing import Optional
from ..models.user_preferences import AIProvider


class UserPreferencesUpdate(BaseModel):
    """Schema for updating user preferences"""
    ai_model_provider: Optional[AIProvider] = None
    ai_model_name: Optional[str] = None
    daily_run_time: Optional[time] = None
    timezone: Optional[str] = None
    auto_run_enabled: Optional[bool] = None
    twitter_list_url: Optional[str] = None
    max_tweets_to_scrape: Optional[str] = None


class UserPreferencesResponse(BaseModel):
    """Schema for user preferences response"""
    id: UUID
    user_id: UUID
    ai_model_provider: AIProvider
    ai_model_name: str
    daily_run_time: time
    timezone: str
    auto_run_enabled: bool
    twitter_list_url: Optional[str]
    max_tweets_to_scrape: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
