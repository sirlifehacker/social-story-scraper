"""API Key model"""
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..database import Base


class ServiceName(str, enum.Enum):
    """Enum for API service names"""
    APIFY = "apify"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE_AI = "google_ai"
    PERPLEXITY = "perplexity"
    TELEGRAM = "telegram"
    NOTION = "notion"


class APIKey(Base):
    """API Key model for storing encrypted service credentials"""

    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    service_name = Column(Enum(ServiceName), nullable=False)
    encrypted_key = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="api_keys")
