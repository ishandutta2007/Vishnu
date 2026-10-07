"""Project Vishnu — Relationship Pydantic Schemas

Request / response models for the Relationship CRUD API.
"""
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class RelationshipCreate(BaseModel):
    """Payload to create a relationship between two entities."""
    source_entity_id: str
    target_entity_id: str
    relationship_type: str = Field(..., description="e.g. ASSOCIATED_WITH, WORKS_FOR, FUNDED_BY")
    properties: dict[str, Any] = Field(default_factory=dict)
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    source: str = "manual"


class RelationshipResponse(BaseModel):
    """Single relationship in API responses."""
    id: str
    source_entity_id: str
    target_entity_id: str
    relationship_type: str
    properties: dict[str, Any]
    confidence_score: float
    source: str
    first_seen: datetime
    last_seen: datetime

    model_config = {"from_attributes": True}


class RelationshipListResponse(BaseModel):
    """List of relationships."""
    total: int
    relationships: list[RelationshipResponse]
