"""API Key schemas"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from ..models.api_key import ServiceName


class APIKeyCreate(BaseModel):
    """Schema for creating API key"""
    service_name: ServiceName
    api_key: str  # Plain text key (will be encrypted before storage)


class APIKeyUpdate(BaseModel):
    """Schema for updating API key"""
    api_key: str
    is_active: bool = True


class APIKeyResponse(BaseModel):
    """Schema for API key response"""
    id: UUID
    service_name: ServiceName
    is_active: bool
    created_at: datetime
    # Note: encrypted_key is never returned to client

    class Config:
        from_attributes = True
