"""Project Vishnu — Entity ORM Model

The Entity table is the heart of the Vishnu ontology.  Every intelligence
object (person, organisation, location, vehicle, event, document) is stored
as a row in this table.  Type-specific attributes live in the JSON
``properties`` column so the schema stays flexible without migrations.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Index, String, Text
from sqlalchemy.orm import relationship as sa_relationship

from app.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _new_id() -> str:
    return str(uuid.uuid4())


class Entity(Base):
    """Core entity table — persons, organisations, locations, etc."""

    __tablename__ = "entities"

    id = Column(String(36), primary_key=True, default=_new_id)
    entity_type = Column(String(20), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, default="")
    properties = Column(Text, default="{}")       # JSON blob for flexible fields
    tags = Column(Text, default="[]")             # JSON list of tags
    confidence_score = Column(Float, default=1.0)
    source = Column(String(255), default="manual")
    classification_level = Column(String(20), default="UNCLASSIFIED")
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    # ── Relationships (ORM) ──────────────────────────────────────────────
    outgoing_relationships = sa_relationship(
        "Relationship",
        foreign_keys="Relationship.source_entity_id",
        back_populates="source_entity",
        cascade="all, delete-orphan",
    )
    incoming_relationships = sa_relationship(
        "Relationship",
        foreign_keys="Relationship.target_entity_id",
        back_populates="target_entity",
        cascade="all, delete-orphan",
    )

    # ── Indexes ──────────────────────────────────────────────────────────
    __table_args__ = (
        Index("idx_entity_type_name", "entity_type", "name"),
    )

    def __repr__(self) -> str:
        return f"<Entity {self.entity_type}:{self.name} ({self.id[:8]})>"
