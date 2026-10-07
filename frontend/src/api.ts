/**
 * Project Vishnu — API Client
 *
 * Centralised API client for communicating with the FastAPI backend.
 */
import type {
  Entity,
  EntityCreate,
  EntityDetail,
  EntityListResponse,
  GraphData,
  SearchResponse,
  CentralityResult,
  Community,
  RelationshipCreate,
  Relationship,
} from './types';

const BASE_URL = '/api';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || `HTTP ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

// ── Entities ────────────────────────────────────────────────────────────────

export const api = {
  // Entities
  listEntities: (params?: { entity_type?: string; search?: string; page?: number; page_size?: number }) => {
    const searchParams = new URLSearchParams();
    if (params?.entity_type) searchParams.set('entity_type', params.entity_type);
    if (params?.search) searchParams.set('search', params.search);
    if (params?.page) searchParams.set('page', String(params.page));
    if (params?.page_size) searchParams.set('page_size', String(params.page_size));
    const qs = searchParams.toString();
    return request<EntityListResponse>(`/entities${qs ? '?' + qs : ''}`);
  },

  getEntity: (id: string) => request<EntityDetail>(`/entities/${id}`),

  createEntity: (data: EntityCreate) =>
    request<Entity>('/entities', { method: 'POST', body: JSON.stringify(data) }),

  deleteEntity: (id: string) =>
    request<void>(`/entities/${id}`, { method: 'DELETE' }),

  // Relationships
  createRelationship: (data: RelationshipCreate) =>
    request<Relationship>('/relationships', { method: 'POST', body: JSON.stringify(data) }),

  deleteRelationship: (id: string) =>
    request<void>(`/relationships/${id}`, { method: 'DELETE' }),

  // Graph
  getGraphData: () => request<GraphData>('/graph/data'),

  getNeighbors: (entityId: string, depth = 1) =>
    request<GraphData>(`/graph/neighbors/${entityId}?depth=${depth}`),

  getShortestPath: (sourceId: string, targetId: string) =>
    request<{ path: string[]; length: number; subgraph: GraphData }>(
      `/graph/shortest-path?source=${sourceId}&target=${targetId}`
    ),

  getCentrality: (topN = 10) =>
    request<CentralityResult[]>(`/graph/centrality?top_n=${topN}`),

  getCommunities: () => request<Community[]>('/graph/communities'),

  // Search
  search: (query: string, entityType?: string) => {
    const params = new URLSearchParams({ q: query });
    if (entityType) params.set('entity_type', entityType);
    return request<SearchResponse>(`/search?${params.toString()}`);
  },

  // Ingestion
  seedData: () => request<{ message: string; seeded: boolean }>('/ingest/seed', { method: 'POST' }),
};
