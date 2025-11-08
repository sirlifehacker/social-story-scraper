"""Content Idea schemas"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any


class ContentIdeaResponse(BaseModel):
    """Schema for content idea response"""
    id: UUID
    scrape_job_id: UUID
    title: str
    content_overview: str
    target_audience: Optional[str]
    core_pain_point: Optional[str]
    hook_strategy: Optional[Dict[str, Any]]
    storyline_outline: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True
