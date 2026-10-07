"""Project Vishnu — Entity Resolution Service

Basic entity resolution using name similarity (difflib SequenceMatcher).
Finds potential duplicate entities and allows merging them.
"""
from __future__ import annotations

import json
from difflib import SequenceMatcher
from typing import Any

from sqlalchemy.orm import Session

from app.models.entity import Entity
from app.models.relationship import Relationship


def find_duplicates(
    db: Session,
    threshold: float = 0.80,
    entity_type: str | None = None,
) -> list[dict[str, Any]]:
    """Find groups of potentially duplicate entities.

    Compares entity names within the same entity_type using
    SequenceMatcher and groups those above the similarity *threshold*.
    """
    query = db.query(Entity)
    if entity_type:
        query = query.filter(Entity.entity_type == entity_type)
    entities = query.all()

    # Group by entity_type for comparison
    by_type: dict[str, list[Entity]] = {}
    for e in entities:
        by_type.setdefault(e.entity_type, []).append(e)

    duplicate_groups: list[dict[str, Any]] = []

    for etype, ents in by_type.items():
        seen: set[str] = set()
        for i, a in enumerate(ents):
            if a.id in seen:
                continue
            group = [a]
            for b in ents[i + 1:]:
                if b.id in seen:
                    continue
                ratio = SequenceMatcher(None, a.name.lower(), b.name.lower()).ratio()
                if ratio >= threshold:
                    group.append(b)
                    seen.add(b.id)
            if len(group) > 1:
                seen.add(a.id)
                duplicate_groups.append({
                    "entity_type": etype,
                    "similarity_threshold": threshold,
                    "entities": [
                        {
                            "id": e.id,
                            "name": e.name,
                            "source": e.source,
                            "confidence_score": e.confidence_score,
                        }
                        for e in group
                    ],
                })

    return duplicate_groups


def merge_entities(db: Session, keep_id: str, merge_id: str) -> dict[str, Any]:
    """Merge *merge_id* into *keep_id*.

    - All relationships pointing to/from *merge_id* are re-pointed to *keep_id*.
    - Tags and properties of *merge_id* are merged into *keep_id*.
    - *merge_id* is deleted.
    """
    keep = db.query(Entity).filter(Entity.id == keep_id).first()
    merge = db.query(Entity).filter(Entity.id == merge_id).first()

    if not keep or not merge:
        return {"error": "One or both entities not found."}

    if keep.entity_type != merge.entity_type:
        return {"error": "Cannot merge entities of different types."}

    # Merge properties
    keep_props = json.loads(keep.properties) if isinstance(keep.properties, str) else keep.properties
    merge_props = json.loads(merge.properties) if isinstance(merge.properties, str) else merge.properties
    for k, v in merge_props.items():
        if k not in keep_props:
            keep_props[k] = v
    keep.properties = json.dumps(keep_props)

    # Merge tags
    keep_tags = json.loads(keep.tags) if isinstance(keep.tags, str) else keep.tags
    merge_tags = json.loads(merge.tags) if isinstance(merge.tags, str) else merge.tags
    keep.tags = json.dumps(list(set(keep_tags + merge_tags)))

    # Re-point relationships
    db.query(Relationship).filter(
        Relationship.source_entity_id == merge_id
    ).update({"source_entity_id": keep_id})
    db.query(Relationship).filter(
        Relationship.target_entity_id == merge_id
    ).update({"target_entity_id": keep_id})

    # Delete the merged entity
    db.delete(merge)
    db.commit()
    db.refresh(keep)

    return {
        "message": f"Entity '{merge.name}' merged into '{keep.name}'.",
        "kept_entity_id": keep_id,
        "deleted_entity_id": merge_id,
    }
