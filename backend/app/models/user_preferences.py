"""User Preferences model"""
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Time, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..database import Base


class AIProvider(str, enum.Enum):
    """Enum for AI model providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"


class UserPreferences(Base):
    """User preferences for scraping and AI configuration"""

    __tablename__ = "user_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)

    # AI Model preferences
    ai_model_provider = Column(Enum(AIProvider), default=AIProvider.OPENAI)
    ai_model_name = Column(String, default="gpt-4-turbo")

    # Scheduling preferences
    daily_run_time = Column(Time, default=func.time("06:45:00"))
    timezone = Column(String, default="America/New_York")
    auto_run_enabled = Column(Boolean, default=True)

    # Twitter/X configuration
    twitter_list_url = Column(String, nullable=True)
    max_tweets_to_scrape = Column(String, default="50")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="preferences")
