"""Project Vishnu — Search Engine Service

Full-text search across all entities using SQLite LIKE queries.
(Lightweight approach that works out of the box — no external search engine needed.)
"""
from __future__ import annotations

import json
from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.entity import Entity


def search_entities(
    db: Session,
    query: str,
    entity_type: str | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Search entities by name, description, or properties content.

    Uses SQL LIKE for simplicity — scales well for < 100k entities.
    """
    pattern = f"%{query}%"

    filters = [
        Entity.name.ilike(pattern),
        Entity.description.ilike(pattern),
        Entity.properties.ilike(pattern),
        Entity.tags.ilike(pattern),
    ]

    q = db.query(Entity).filter(or_(*filters))

    if entity_type:
        q = q.filter(Entity.entity_type == entity_type)

    results = q.limit(limit).all()

    return [
        {
            "id": e.id,
            "entity_type": e.entity_type,
            "name": e.name,
            "description": e.description,
            "confidence_score": e.confidence_score,
            "classification_level": e.classification_level,
            "source": e.source,
            "tags": json.loads(e.tags) if isinstance(e.tags, str) else e.tags,
        }
        for e in results
    ]
