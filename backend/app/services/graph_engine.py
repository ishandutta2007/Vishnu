"""Project Vishnu — Graph Analytics Engine

Builds an in-memory NetworkX graph from the database and exposes analytics
such as shortest-path, centrality, community detection, and neighbor expansion.
"""
from __future__ import annotations

import json
from typing import Any

import networkx as nx
from sqlalchemy.orm import Session

from app.models.entity import Entity
from app.models.relationship import Relationship


class GraphEngine:
    """Wraps NetworkX to provide intelligence-oriented graph analytics."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.G = nx.Graph()
        self._build()

    # ── Graph Construction ───────────────────────────────────────────────

    def _build(self) -> None:
        """Load entities and relationships from DB into the NetworkX graph."""
        entities = self.db.query(Entity).all()
        relationships = self.db.query(Relationship).all()

        for e in entities:
            props = json.loads(e.properties) if isinstance(e.properties, str) else e.properties
            self.G.add_node(
                e.id,
                label=e.name,
                entity_type=e.entity_type,
                description=e.description or "",
                confidence=e.confidence_score,
                classification=e.classification_level,
                properties=props,
                tags=json.loads(e.tags) if isinstance(e.tags, str) else e.tags,
            )

        for r in relationships:
            props = json.loads(r.properties) if isinstance(r.properties, str) else r.properties
            self.G.add_edge(
                r.source_entity_id,
                r.target_entity_id,
                id=r.id,
                relationship_type=r.relationship_type,
                confidence=r.confidence_score,
                properties=props,
            )

    # ── Full Graph Data (Cytoscape.js compatible) ────────────────────────

    def get_graph_data(self) -> dict[str, list[dict]]:
        """Return the full graph in Cytoscape.js elements format."""
        nodes = []
        for nid, data in self.G.nodes(data=True):
            nodes.append({
                "data": {
                    "id": nid,
                    "label": data.get("label", ""),
                    "entity_type": data.get("entity_type", ""),
                    "description": data.get("description", ""),
                    "confidence": data.get("confidence", 1.0),
                    "classification": data.get("classification", "UNCLASSIFIED"),
                    "properties": data.get("properties", {}),
                    "tags": data.get("tags", []),
                }
            })

        edges = []
        for u, v, data in self.G.edges(data=True):
            edges.append({
                "data": {
                    "id": data.get("id", f"{u}-{v}"),
                    "source": u,
                    "target": v,
                    "label": data.get("relationship_type", ""),
                    "relationship_type": data.get("relationship_type", ""),
                    "confidence": data.get("confidence", 1.0),
                    "properties": data.get("properties", {}),
                }
            })

        return {"nodes": nodes, "edges": edges}

    # ── Neighbor Expansion ───────────────────────────────────────────────

    def get_neighbors(self, entity_id: str, depth: int = 1) -> dict[str, list[dict]]:
        """Return the sub-graph within *depth* hops of *entity_id*."""
        if entity_id not in self.G:
            return {"nodes": [], "edges": []}

        # BFS to depth
        visited: set[str] = set()
        frontier = {entity_id}
        for _ in range(depth):
            next_frontier: set[str] = set()
            for n in frontier:
                visited.add(n)
                next_frontier.update(self.G.neighbors(n))
            frontier = next_frontier - visited
        visited.update(frontier)

        sub = self.G.subgraph(visited)
        return self._subgraph_to_cytoscape(sub)

    # ── Shortest Path ────────────────────────────────────────────────────

    def shortest_path(self, source_id: str, target_id: str) -> dict[str, Any]:
        """Find the shortest path between two entities."""
        if source_id not in self.G or target_id not in self.G:
            return {"path": [], "length": -1, "subgraph": {"nodes": [], "edges": []}}

        try:
            path = nx.shortest_path(self.G, source_id, target_id)
        except nx.NetworkXNoPath:
            return {"path": [], "length": -1, "subgraph": {"nodes": [], "edges": []}}

        sub = self.G.subgraph(path)
        return {
            "path": path,
            "length": len(path) - 1,
            "subgraph": self._subgraph_to_cytoscape(sub),
        }

    # ── Centrality ───────────────────────────────────────────────────────

    def betweenness_centrality(self, top_n: int = 10) -> list[dict[str, Any]]:
        """Return the top-N entities by betweenness centrality."""
        if len(self.G) == 0:
            return []

        centrality = nx.betweenness_centrality(self.G)
        sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:top_n]

        results = []
        for nid, score in sorted_nodes:
            data = self.G.nodes[nid]
            results.append({
                "id": nid,
                "label": data.get("label", ""),
                "entity_type": data.get("entity_type", ""),
                "centrality_score": round(score, 6),
            })
        return results

    # ── Community Detection ──────────────────────────────────────────────

    def detect_communities(self) -> list[dict[str, Any]]:
        """Detect communities using greedy modularity optimisation."""
        if len(self.G) == 0:
            return []

        communities = nx.community.greedy_modularity_communities(self.G)

        results = []
        for idx, community in enumerate(communities):
            members = []
            for nid in community:
                data = self.G.nodes[nid]
                members.append({
                    "id": nid,
                    "label": data.get("label", ""),
                    "entity_type": data.get("entity_type", ""),
                })
            results.append({
                "community_id": idx,
                "size": len(community),
                "members": members,
            })
        return results

    # ── Helpers ──────────────────────────────────────────────────────────

    def _subgraph_to_cytoscape(self, sub: nx.Graph) -> dict[str, list[dict]]:
        """Convert a NetworkX subgraph to Cytoscape.js elements format."""
        nodes = []
        for nid, data in sub.nodes(data=True):
            nodes.append({
                "data": {
                    "id": nid,
                    "label": data.get("label", ""),
                    "entity_type": data.get("entity_type", ""),
                    "description": data.get("description", ""),
                    "confidence": data.get("confidence", 1.0),
                    "classification": data.get("classification", "UNCLASSIFIED"),
                }
            })
        edges = []
        for u, v, data in sub.edges(data=True):
            edges.append({
                "data": {
                    "id": data.get("id", f"{u}-{v}"),
                    "source": u,
                    "target": v,
                    "label": data.get("relationship_type", ""),
                    "relationship_type": data.get("relationship_type", ""),
                    "confidence": data.get("confidence", 1.0),
                }
            })
        return {"nodes": nodes, "edges": edges}
