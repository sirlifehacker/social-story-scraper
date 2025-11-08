"""Tweet schemas"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class TweetResponse(BaseModel):
    """Schema for tweet response"""
    id: UUID
    scrape_job_id: UUID
    tweet_id: str
    text: str
    url: str
    author_username: Optional[str]
    author_follower_count: Optional[int]
    like_count: int
    retweet_count: int
    reply_count: int
    engagement_score: float
    created_at: datetime

    class Config:
        from_attributes = True
