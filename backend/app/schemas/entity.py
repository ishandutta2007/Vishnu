"""Project Vishnu — Entity Pydantic Schemas

Request / response models for the Entity CRUD API.
"""
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ── Creation & Update ────────────────────────────────────────────────────────

class EntityCreate(BaseModel):
    """Payload to create a new entity."""
    entity_type: str = Field(..., description="One of: person, organization, location, vehicle, event, document")
    name: str = Field(..., min_length=1, max_length=255)
    description: str = ""
    properties: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    source: str = "manual"
    classification_level: str = "UNCLASSIFIED"


class EntityUpdate(BaseModel):
    """Payload to update an existing entity (partial)."""
    name: str | None = None
    description: str | None = None
    properties: dict[str, Any] | None = None
    tags: list[str] | None = None
    confidence_score: float | None = Field(default=None, ge=0.0, le=1.0)
    source: str | None = None
    classification_level: str | None = None


# ── Responses ────────────────────────────────────────────────────────────────

class EntityResponse(BaseModel):
    """Single entity in API responses."""
    id: str
    entity_type: str
    name: str
    description: str
    properties: dict[str, Any]
    tags: list[str]
    confidence_score: float
    source: str
    classification_level: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EntityDetailResponse(EntityResponse):
    """Entity with its relationships included."""
    outgoing_relationships: list["RelationshipBrief"] = []
    incoming_relationships: list["RelationshipBrief"] = []


class RelationshipBrief(BaseModel):
    """Minimal relationship info embedded in entity detail."""
    id: str
    relationship_type: str
    source_entity_id: str
    target_entity_id: str
    confidence_score: float

    model_config = {"from_attributes": True}


class EntityListResponse(BaseModel):
    """Paginated list of entities."""
    total: int
    page: int
    page_size: int
    entities: list[EntityResponse]


# Rebuild forward refs
EntityDetailResponse.model_rebuild()
