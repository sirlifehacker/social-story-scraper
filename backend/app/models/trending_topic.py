"""Trending Topic model"""
import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class TrendingTopic(Base):
    """Trending topic identified by AI analysis"""

    __tablename__ = "trending_topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scrape_job_id = Column(UUID(as_uuid=True), ForeignKey("scrape_jobs.id"), nullable=False)

    rank = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    # Perplexity research data
    key_insights = Column(Text, nullable=True)
    visual_analogy = Column(Text, nullable=True)
    most_benefited_niches = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    scrape_job = relationship("ScrapeJob", back_populates="trending_topics")
