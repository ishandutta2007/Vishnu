/**
 * Project Vishnu — TypeScript Type Definitions
 *
 * Shared types matching the backend Pydantic schemas.
 */

// ── Entity Types ────────────────────────────────────────────────────────────

export type EntityType = 'person' | 'organization' | 'location' | 'vehicle' | 'event' | 'document';

export type ClassificationLevel = 'UNCLASSIFIED' | 'RESTRICTED' | 'CONFIDENTIAL' | 'SECRET' | 'TOP_SECRET';

export interface Entity {
  id: string;
  entity_type: EntityType;
  name: string;
  description: string;
  properties: Record<string, unknown>;
  tags: string[];
  confidence_score: number;
  source: string;
  classification_level: ClassificationLevel;
  created_at: string;
  updated_at: string;
}

export interface EntityDetail extends Entity {
  outgoing_relationships: RelationshipBrief[];
  incoming_relationships: RelationshipBrief[];
}

export interface EntityCreate {
  entity_type: EntityType;
  name: string;
  description?: string;
  properties?: Record<string, unknown>;
  tags?: string[];
  confidence_score?: number;
  source?: string;
  classification_level?: ClassificationLevel;
}

export interface EntityListResponse {
  total: number;
  page: number;
  page_size: number;
  entities: Entity[];
}

// ── Relationship Types ──────────────────────────────────────────────────────

export interface RelationshipBrief {
  id: string;
  relationship_type: string;
  source_entity_id: string;
  target_entity_id: string;
  confidence_score: number;
}

export interface Relationship {
  id: string;
  source_entity_id: string;
  target_entity_id: string;
  relationship_type: string;
  properties: Record<string, unknown>;
  confidence_score: number;
  source: string;
  first_seen: string;
  last_seen: string;
}

export interface RelationshipCreate {
  source_entity_id: string;
  target_entity_id: string;
  relationship_type: string;
  properties?: Record<string, unknown>;
  confidence_score?: number;
  source?: string;
}

// ── Graph Types (Cytoscape.js compatible) ───────────────────────────────────

export interface CytoscapeNodeData {
  id: string;
  label: string;
  entity_type: EntityType;
  description?: string;
  confidence?: number;
  classification?: ClassificationLevel;
  properties?: Record<string, unknown>;
  tags?: string[];
}

export interface CytoscapeEdgeData {
  id: string;
  source: string;
  target: string;
  label: string;
  relationship_type: string;
  confidence?: number;
  properties?: Record<string, unknown>;
}

export interface CytoscapeNode {
  data: CytoscapeNodeData;
}

export interface CytoscapeEdge {
  data: CytoscapeEdgeData;
}

export interface GraphData {
  nodes: CytoscapeNode[];
  edges: CytoscapeEdge[];
}

// ── Search Types ────────────────────────────────────────────────────────────

export interface SearchResult {
  id: string;
  entity_type: EntityType;
  name: string;
  description: string;
  confidence_score: number;
  classification_level: ClassificationLevel;
  source: string;
  tags: string[];
}

export interface SearchResponse {
  query: string;
  total: number;
  results: SearchResult[];
}

// ── Analytics Types ─────────────────────────────────────────────────────────

export interface CentralityResult {
  id: string;
  label: string;
  entity_type: EntityType;
  centrality_score: number;
}

export interface CommunityMember {
  id: string;
  label: string;
  entity_type: EntityType;
}

export interface Community {
  community_id: number;
  size: number;
  members: CommunityMember[];
}
