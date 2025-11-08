"""Trending Topic schemas"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class TrendingTopicResponse(BaseModel):
    """Schema for trending topic response"""
    id: UUID
    scrape_job_id: UUID
    rank: int
    title: str
    description: str
    key_insights: Optional[str]
    visual_analogy: Optional[str]
    most_benefited_niches: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
