"""Project Vishnu — Graph Analytics Router

Endpoints for graph visualisation data and analytics
(shortest path, centrality, community detection, neighbor expansion).
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.graph_engine import GraphEngine

router = APIRouter(prefix="/graph", tags=["Graph Analytics"])


@router.get("/data")
def get_graph_data(db: Session = Depends(get_db)) -> dict[str, Any]:
    """Return the full graph in Cytoscape.js-compatible format."""
    engine = GraphEngine(db)
    return engine.get_graph_data()


@router.get("/neighbors/{entity_id}")
def get_neighbors(
    entity_id: str,
    depth: int = Query(1, ge=1, le=5, description="Number of hops"),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Get sub-graph within N hops of an entity."""
    engine = GraphEngine(db)
    return engine.get_neighbors(entity_id, depth=depth)


@router.get("/shortest-path")
def shortest_path(
    source: str = Query(..., description="Source entity ID"),
    target: str = Query(..., description="Target entity ID"),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Find the shortest path between two entities."""
    engine = GraphEngine(db)
    return engine.shortest_path(source, target)


@router.get("/centrality")
def centrality(
    top_n: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    """Get top-N entities by betweenness centrality."""
    engine = GraphEngine(db)
    return engine.betweenness_centrality(top_n=top_n)


@router.get("/communities")
def communities(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    """Detect communities using greedy modularity optimisation."""
    engine = GraphEngine(db)
    return engine.detect_communities()
