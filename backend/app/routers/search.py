"""Project Vishnu — Search Router

Full-text search across all entities.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.search_engine import search_entities

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("")
def search(
    q: str = Query(..., min_length=1, description="Search query"),
    entity_type: str | None = Query(None, description="Filter by entity type"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Search entities by name, description, or properties."""
    results = search_entities(db, query=q, entity_type=entity_type, limit=limit)
    return {"query": q, "total": len(results), "results": results}
