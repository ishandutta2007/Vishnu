"""Project Vishnu — Entity CRUD Router

Endpoints for creating, reading, updating, and deleting entities,
plus entity-resolution helpers (find duplicates, merge).
"""
from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.entity import Entity
from app.schemas.entity import (
    EntityCreate,
    EntityDetailResponse,
    EntityListResponse,
    EntityResponse,
    EntityUpdate,
    RelationshipBrief,
)
from app.services.entity_resolution import find_duplicates, merge_entities

router = APIRouter(prefix="/entities", tags=["Entities"])


# ── Helpers ──────────────────────────────────────────────────────────────────

def _entity_to_response(e: Entity) -> EntityResponse:
    """Convert an ORM Entity to the API response schema."""
    return EntityResponse(
        id=e.id,
        entity_type=e.entity_type,
        name=e.name,
        description=e.description or "",
        properties=json.loads(e.properties) if isinstance(e.properties, str) else e.properties,
        tags=json.loads(e.tags) if isinstance(e.tags, str) else e.tags,
        confidence_score=e.confidence_score,
        source=e.source,
        classification_level=e.classification_level,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )


# ── CRUD ─────────────────────────────────────────────────────────────────────

@router.get("", response_model=EntityListResponse)
def list_entities(
    entity_type: str | None = Query(None, description="Filter by entity type"),
    search: str | None = Query(None, description="Search by name"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> EntityListResponse:
    """List all entities with optional filtering and pagination."""
    q = db.query(Entity)
    if entity_type:
        q = q.filter(Entity.entity_type == entity_type)
    if search:
        q = q.filter(Entity.name.ilike(f"%{search}%"))

    total = q.count()
    entities = q.order_by(Entity.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return EntityListResponse(
        total=total,
        page=page,
        page_size=page_size,
        entities=[_entity_to_response(e) for e in entities],
    )


@router.get("/{entity_id}", response_model=EntityDetailResponse)
def get_entity(entity_id: str, db: Session = Depends(get_db)) -> EntityDetailResponse:
    """Get a single entity with its relationships."""
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    resp = _entity_to_response(entity)
    detail = EntityDetailResponse(**resp.model_dump())

    detail.outgoing_relationships = [
        RelationshipBrief(
            id=r.id,
            relationship_type=r.relationship_type,
            source_entity_id=r.source_entity_id,
            target_entity_id=r.target_entity_id,
            confidence_score=r.confidence_score,
        )
        for r in entity.outgoing_relationships
    ]
    detail.incoming_relationships = [
        RelationshipBrief(
            id=r.id,
            relationship_type=r.relationship_type,
            source_entity_id=r.source_entity_id,
            target_entity_id=r.target_entity_id,
            confidence_score=r.confidence_score,
        )
        for r in entity.incoming_relationships
    ]

    return detail


@router.post("", response_model=EntityResponse, status_code=201)
def create_entity(payload: EntityCreate, db: Session = Depends(get_db)) -> EntityResponse:
    """Create a new entity."""
    entity = Entity(
        entity_type=payload.entity_type,
        name=payload.name,
        description=payload.description,
        properties=json.dumps(payload.properties),
        tags=json.dumps(payload.tags),
        confidence_score=payload.confidence_score,
        source=payload.source,
        classification_level=payload.classification_level,
    )
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return _entity_to_response(entity)


@router.put("/{entity_id}", response_model=EntityResponse)
def update_entity(
    entity_id: str,
    payload: EntityUpdate,
    db: Session = Depends(get_db),
) -> EntityResponse:
    """Update an existing entity (partial update)."""
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "properties" in update_data:
        update_data["properties"] = json.dumps(update_data["properties"])
    if "tags" in update_data:
        update_data["tags"] = json.dumps(update_data["tags"])

    for key, value in update_data.items():
        setattr(entity, key, value)

    db.commit()
    db.refresh(entity)
    return _entity_to_response(entity)


@router.delete("/{entity_id}", status_code=204)
def delete_entity(entity_id: str, db: Session = Depends(get_db)) -> None:
    """Delete an entity and its relationships."""
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    db.delete(entity)
    db.commit()


# ── Entity Resolution ────────────────────────────────────────────────────────

@router.get("/duplicates/detect", response_model=list[dict[str, Any]])
def detect_duplicates(
    threshold: float = Query(0.80, ge=0.5, le=1.0, description="Similarity threshold (0.5-1.0)"),
    entity_type: str | None = Query(None),
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    """Find groups of potentially duplicate entities based on name similarity."""
    return find_duplicates(db, threshold=threshold, entity_type=entity_type)


@router.post("/merge")
def merge(
    keep_id: str = Query(..., description="ID of the entity to keep"),
    merge_id: str = Query(..., description="ID of the entity to merge (will be deleted)"),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Merge two duplicate entities into one."""
    result = merge_entities(db, keep_id, merge_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
