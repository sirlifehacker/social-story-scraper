"""Content Idea model"""
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class ContentIdea(Base):
    """AI-generated content idea"""

    __tablename__ = "content_ideas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scrape_job_id = Column(UUID(as_uuid=True), ForeignKey("scrape_jobs.id"), nullable=False)

    title = Column(String, nullable=False)
    content_overview = Column(Text, nullable=False)

    # Target audience analysis
    target_audience = Column(Text, nullable=True)
    core_pain_point = Column(Text, nullable=True)

    # Strategy data (stored as JSON for flexibility)
    hook_strategy = Column(JSON, nullable=True)
    storyline_outline = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    scrape_job = relationship("ScrapeJob", back_populates="content_ideas")
