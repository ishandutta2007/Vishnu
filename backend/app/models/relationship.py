"""Project Vishnu — Relationship ORM Model

Relationships (edges) connect two Entity rows.  Relationship-specific
metadata is stored in the JSON ``properties`` column.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, String, Text
from sqlalchemy.orm import relationship as sa_relationship

from app.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _new_id() -> str:
    return str(uuid.uuid4())


class Relationship(Base):
    """Directed edge between two entities."""

    __tablename__ = "relationships"

    id = Column(String(36), primary_key=True, default=_new_id)
    source_entity_id = Column(
        String(36), ForeignKey("entities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    target_entity_id = Column(
        String(36), ForeignKey("entities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    relationship_type = Column(String(50), nullable=False, index=True)
    properties = Column(Text, default="{}")   # JSON blob
    confidence_score = Column(Float, default=1.0)
    source = Column(String(255), default="manual")
    first_seen = Column(DateTime, default=_utcnow)
    last_seen = Column(DateTime, default=_utcnow)

    # ── ORM back-references ──────────────────────────────────────────────
    source_entity = sa_relationship(
        "Entity", foreign_keys=[source_entity_id], back_populates="outgoing_relationships"
    )
    target_entity = sa_relationship(
        "Entity", foreign_keys=[target_entity_id], back_populates="incoming_relationships"
    )

    # ── Indexes ──────────────────────────────────────────────────────────
    __table_args__ = (
        Index("idx_rel_pair", "source_entity_id", "target_entity_id"),
    )

    def __repr__(self) -> str:
        return (
            f"<Relationship {self.relationship_type} "
            f"{self.source_entity_id[:8]}→{self.target_entity_id[:8]}>"
        )
