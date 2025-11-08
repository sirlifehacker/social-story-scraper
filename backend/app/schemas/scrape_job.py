"""Scrape Job schemas"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any
from ..models.scrape_job import JobStatus, TriggerType


class ScrapeJobCreate(BaseModel):
    """Schema for creating a scrape job"""
    trigger_type: TriggerType = TriggerType.MANUAL


class ScrapeJobResponse(BaseModel):
    """Schema for scrape job response"""
    id: UUID
    user_id: UUID
    status: JobStatus
    trigger_type: TriggerType
    ai_model_used: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True
