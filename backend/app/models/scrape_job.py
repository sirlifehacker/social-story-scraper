"""Scrape Job model"""
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..database import Base


class JobStatus(str, enum.Enum):
    """Enum for scrape job status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TriggerType(str, enum.Enum):
    """Enum for job trigger type"""
    MANUAL = "manual"
    SCHEDULED = "scheduled"


class ScrapeJob(Base):
    """Scrape job tracking model"""

    __tablename__ = "scrape_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    trigger_type = Column(Enum(TriggerType), nullable=False)
    ai_model_used = Column(String, nullable=True)

    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(String, nullable=True)

    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="scrape_jobs")
    tweets = relationship("Tweet", back_populates="scrape_job", cascade="all, delete-orphan")
    trending_topics = relationship("TrendingTopic", back_populates="scrape_job", cascade="all, delete-orphan")
    content_ideas = relationship("ContentIdea", back_populates="scrape_job", cascade="all, delete-orphan")
