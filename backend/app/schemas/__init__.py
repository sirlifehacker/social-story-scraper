"""Pydantic schemas for API validation"""
from .user import UserCreate, UserLogin, UserResponse, Token, TokenData
from .api_key import APIKeyCreate, APIKeyUpdate, APIKeyResponse
from .preferences import UserPreferencesUpdate, UserPreferencesResponse
from .scrape_job import ScrapeJobCreate, ScrapeJobResponse
from .tweet import TweetResponse
from .trending_topic import TrendingTopicResponse
from .content_idea import ContentIdeaResponse

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "Token",
    "TokenData",
    "APIKeyCreate",
    "APIKeyUpdate",
    "APIKeyResponse",
    "UserPreferencesUpdate",
    "UserPreferencesResponse",
    "ScrapeJobCreate",
    "ScrapeJobResponse",
    "TweetResponse",
    "TrendingTopicResponse",
    "ContentIdeaResponse",
]
