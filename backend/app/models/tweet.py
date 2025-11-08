"""Tweet model"""
import uuid
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Tweet(Base):
    """Tweet/X post model"""

    __tablename__ = "tweets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scrape_job_id = Column(UUID(as_uuid=True), ForeignKey("scrape_jobs.id"), nullable=False)

    # Tweet data
    tweet_id = Column(String, unique=True, index=True, nullable=False)
    text = Column(String, nullable=False)
    url = Column(String, nullable=False)

    # Author info
    author_username = Column(String, nullable=True)
    author_follower_count = Column(Integer, nullable=True)

    # Engagement metrics
    like_count = Column(Integer, default=0)
    retweet_count = Column(Integer, default=0)
    reply_count = Column(Integer, default=0)
    engagement_score = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    scrape_job = relationship("ScrapeJob", back_populates="tweets")
