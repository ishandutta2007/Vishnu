"""Project Vishnu — Data Ingestion Router

Upload CSV or JSON files to bulk-create entities and relationships.
Also provides a one-click seed data loader for the demo scenario.
"""
from __future__ import annotations

import csv
import io
import json
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.entity import Entity
from app.models.relationship import Relationship

router = APIRouter(prefix="/ingest", tags=["Data Ingestion"])


@router.post("/csv")
async def ingest_csv(
    file: UploadFile = File(..., description="CSV file with entity data"),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Ingest entities from a CSV file.

    Expected columns: entity_type, name, description, source, confidence_score,
    classification_level, and any additional columns become properties.
    """
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a .csv")

    content = await file.read()
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))

    core_fields = {
        "entity_type", "name", "description", "source",
        "confidence_score", "classification_level", "tags",
    }

    created = 0
    for row in reader:
        if "name" not in row or "entity_type" not in row:
            continue

        # Extra columns go into properties
        props = {k: v for k, v in row.items() if k not in core_fields and v}
        tags = [t.strip() for t in row.get("tags", "").split(",") if t.strip()]

        entity = Entity(
            entity_type=row["entity_type"].strip().lower(),
            name=row["name"].strip(),
            description=row.get("description", "").strip(),
            source=row.get("source", "csv_import").strip(),
            confidence_score=float(row.get("confidence_score", 1.0)),
            classification_level=row.get("classification_level", "UNCLASSIFIED").strip(),
            properties=json.dumps(props),
            tags=json.dumps(tags),
        )
        db.add(entity)
        created += 1

    db.commit()
    return {"message": f"Successfully ingested {created} entities from CSV.", "count": created}


@router.post("/json")
async def ingest_json(
    file: UploadFile = File(..., description="JSON file with entities and/or relationships"),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Ingest entities and relationships from a JSON file.

    Expected format:
    {
      "entities": [ { "entity_type": "person", "name": "...", ... } ],
      "relationships": [ { "source_name": "...", "target_name": "...",
                            "relationship_type": "...", ... } ]
    }
    """
    if not file.filename or not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="File must be a .json")

    content = await file.read()
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    entities_created = 0
    rels_created = 0
    name_to_id: dict[str, str] = {}

    # Import entities
    for e in data.get("entities", []):
        entity = Entity(
            entity_type=e.get("entity_type", "person"),
            name=e["name"],
            description=e.get("description", ""),
            properties=json.dumps(e.get("properties", {})),
            tags=json.dumps(e.get("tags", [])),
            confidence_score=e.get("confidence_score", 1.0),
            source=e.get("source", "json_import"),
            classification_level=e.get("classification_level", "UNCLASSIFIED"),
        )
        db.add(entity)
        db.flush()  # Get the generated ID
        name_to_id[e["name"]] = entity.id
        entities_created += 1

    # Import relationships (by name lookup)
    for r in data.get("relationships", []):
        src_id = name_to_id.get(r.get("source_name", ""))
        tgt_id = name_to_id.get(r.get("target_name", ""))
        if not src_id or not tgt_id:
            continue

        rel = Relationship(
            source_entity_id=src_id,
            target_entity_id=tgt_id,
            relationship_type=r.get("relationship_type", "RELATED_TO"),
            properties=json.dumps(r.get("properties", {})),
            confidence_score=r.get("confidence_score", 1.0),
            source=r.get("source", "json_import"),
        )
        db.add(rel)
        rels_created += 1

    db.commit()
    return {
        "message": f"Ingested {entities_created} entities and {rels_created} relationships.",
        "entities_created": entities_created,
        "relationships_created": rels_created,
    }


@router.post("/seed")
def load_seed_data(db: Session = Depends(get_db)) -> dict[str, Any]:
    """Load the built-in demo seed data (Operation Nightfall scenario)."""
    from app.seed_data import seed

    result = seed(db)
    return result
