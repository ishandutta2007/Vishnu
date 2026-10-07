"""Project Vishnu — Relationship CRUD Router

Endpoints for creating, listing, and deleting relationships between entities.
"""
from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.entity import Entity
from app.models.relationship import Relationship
from app.schemas.relationship import (
    RelationshipCreate,
    RelationshipListResponse,
    RelationshipResponse,
)

router = APIRouter(prefix="/relationships", tags=["Relationships"])


def _rel_to_response(r: Relationship) -> RelationshipResponse:
    return RelationshipResponse(
        id=r.id,
        source_entity_id=r.source_entity_id,
        target_entity_id=r.target_entity_id,
        relationship_type=r.relationship_type,
        properties=json.loads(r.properties) if isinstance(r.properties, str) else r.properties,
        confidence_score=r.confidence_score,
        source=r.source,
        first_seen=r.first_seen,
        last_seen=r.last_seen,
    )


@router.get("", response_model=RelationshipListResponse)
def list_relationships(
    relationship_type: str | None = Query(None),
    source_entity_id: str | None = Query(None),
    target_entity_id: str | None = Query(None),
    db: Session = Depends(get_db),
) -> RelationshipListResponse:
    """List relationships with optional filtering."""
    q = db.query(Relationship)
    if relationship_type:
        q = q.filter(Relationship.relationship_type == relationship_type)
    if source_entity_id:
        q = q.filter(Relationship.source_entity_id == source_entity_id)
    if target_entity_id:
        q = q.filter(Relationship.target_entity_id == target_entity_id)

    rels = q.all()
    return RelationshipListResponse(
        total=len(rels),
        relationships=[_rel_to_response(r) for r in rels],
    )


@router.post("", response_model=RelationshipResponse, status_code=201)
def create_relationship(
    payload: RelationshipCreate,
    db: Session = Depends(get_db),
) -> RelationshipResponse:
    """Create a relationship between two entities."""
    # Validate entities exist
    src = db.query(Entity).filter(Entity.id == payload.source_entity_id).first()
    tgt = db.query(Entity).filter(Entity.id == payload.target_entity_id).first()
    if not src:
        raise HTTPException(status_code=404, detail=f"Source entity {payload.source_entity_id} not found")
    if not tgt:
        raise HTTPException(status_code=404, detail=f"Target entity {payload.target_entity_id} not found")

    rel = Relationship(
        source_entity_id=payload.source_entity_id,
        target_entity_id=payload.target_entity_id,
        relationship_type=payload.relationship_type,
        properties=json.dumps(payload.properties),
        confidence_score=payload.confidence_score,
        source=payload.source,
    )
    db.add(rel)
    db.commit()
    db.refresh(rel)
    return _rel_to_response(rel)


@router.delete("/{relationship_id}", status_code=204)
def delete_relationship(relationship_id: str, db: Session = Depends(get_db)) -> None:
    """Delete a relationship."""
    rel = db.query(Relationship).filter(Relationship.id == relationship_id).first()
    if not rel:
        raise HTTPException(status_code=404, detail="Relationship not found")
    db.delete(rel)
    db.commit()
