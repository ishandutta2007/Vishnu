/**
 * Project Vishnu — Main Application Component
 *
 * Orchestrates the entire intelligence workspace:
 *  - Left Sidebar: entity list, search, filters
 *  - Center: interactive graph canvas (Cytoscape.js)
 *  - Right Panel: entity dossier (360° view)
 *  - Top Bar: global search, analytics
 */
import { useState, useEffect, useCallback } from 'react';
import { api } from './api';
import type { Entity, GraphData, CentralityResult, Community } from './types';

import TopBar from './components/TopBar';
import Sidebar from './components/Sidebar';
import GraphWorkspace from './components/GraphWorkspace';
import EntityDossier from './components/EntityDossier';
import CreateEntityModal from './components/CreateEntityModal';

export default function App() {
  // ── State ─────────────────────────────────────────────────────────────
  const [entities, setEntities] = useState<Entity[]>([]);
  const [totalEntities, setTotalEntities] = useState(0);
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [selectedEntityId, setSelectedEntityId] = useState<string | null>(null);
  const [highlightedPath, setHighlightedPath] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  // Analytics
  const [centralityResults, setCentralityResults] = useState<CentralityResult[]>([]);
  const [communityResults, setCommunityResults] = useState<Community[]>([]);
  const [showAnalytics, setShowAnalytics] = useState<'centrality' | 'communities' | null>(null);

  // ── Data Loading ──────────────────────────────────────────────────────

  const loadEntities = useCallback(async (type?: string | null, search?: string) => {
    setIsLoading(true);
    try {
      const params: Record<string, string> = { page_size: '200' };
      if (type) params.entity_type = type;
      if (search) params.search = search;
      const resp = await api.listEntities(params);
      setEntities(resp.entities);
      setTotalEntities(resp.total);
    } catch (err) {
      console.error('Failed to load entities:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const loadGraphData = useCallback(async () => {
    try {
      const data = await api.getGraphData();
      setGraphData(data);
    } catch (err) {
      console.error('Failed to load graph data:', err);
    }
  }, []);

  const refreshAll = useCallback(async () => {
    await Promise.all([loadEntities(), loadGraphData()]);
  }, [loadEntities, loadGraphData]);

  // Initial load
  useEffect(() => {
    refreshAll();
  }, [refreshAll]);

  // ── Handlers ──────────────────────────────────────────────────────────

  const handleSearch = useCallback((query: string) => {
    loadEntities(null, query || undefined);
  }, [loadEntities]);

  const handleFilterType = useCallback((type: string | null) => {
    loadEntities(type);
  }, [loadEntities]);

  const handleEntitySelect = useCallback((id: string) => {
    setSelectedEntityId(id || null);
    setHighlightedPath([]);
  }, []);

  const handleLoadSeedData = useCallback(async () => {
    setIsLoading(true);
    try {
      const result = await api.seedData();
      setStatusMessage(result.message);
      await refreshAll();
      setTimeout(() => setStatusMessage(null), 4000);
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to load seed data';
      setStatusMessage(`Error: ${msg}`);
      setTimeout(() => setStatusMessage(null), 4000);
    } finally {
      setIsLoading(false);
    }
  }, [refreshAll]);

  const handleFindPath = useCallback(async (sourceId: string, targetId: string) => {
    try {
      const result = await api.getShortestPath(sourceId, targetId);
      if (result.path.length > 0) {
        setHighlightedPath(result.path);
        setStatusMessage(`Shortest path found: ${result.length} hop(s)`);
      } else {
        setStatusMessage('No path found between these entities');
      }
      setTimeout(() => setStatusMessage(null), 4000);
    } catch (err) {
      console.error('Failed to find path:', err);
    }
  }, []);

  const handleShowCentrality = useCallback(async () => {
    try {
      const results = await api.getCentrality(10);
      setCentralityResults(results);
      setShowAnalytics('centrality');
    } catch (err) {
      console.error('Failed to load centrality:', err);
    }
  }, []);

  const handleShowCommunities = useCallback(async () => {
    try {
      const results = await api.getCommunities();
      setCommunityResults(results);
      setShowAnalytics('communities');
    } catch (err) {
      console.error('Failed to load communities:', err);
    }
  }, []);

  const handleGlobalSearch = useCallback(async (query: string) => {
    try {
      const results = await api.search(query);
      // Update sidebar with search results converted to entity format
      if (results.results.length > 0) {
        setStatusMessage(`Found ${results.total} result(s) for "${query}"`);
        // Load the matching entities into the sidebar
        loadEntities(null, query);
      } else {
        setStatusMessage(`No results for "${query}"`);
      }
      setTimeout(() => setStatusMessage(null), 4000);
    } catch (err) {
      console.error('Search failed:', err);
    }
  }, [loadEntities]);

  // ── Render ────────────────────────────────────────────────────────────
  return (
    <div className="h-screen flex flex-col overflow-hidden">
      {/* Top Bar */}
      <TopBar
        onGlobalSearch={handleGlobalSearch}
        onShowCentrality={handleShowCentrality}
        onShowCommunities={handleShowCommunities}
        centralityResults={centralityResults}
        communityResults={communityResults}
        showAnalytics={showAnalytics}
        onCloseAnalytics={() => setShowAnalytics(null)}
        onFocusEntity={handleEntitySelect}
      />

      {/* Status Banner */}
      {statusMessage && (
        <div className={`px-4 py-2 text-xs text-center flex-shrink-0 ${
          statusMessage.startsWith('Error')
            ? 'bg-red-900/40 text-red-300 border-b border-red-700'
            : 'bg-vishnu-900/40 text-vishnu-300 border-b border-vishnu-700'
        }`}>
          {statusMessage}
        </div>
      )}

      {/* Main Content Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar */}
        <Sidebar
          entities={entities}
          selectedEntityId={selectedEntityId}
          onEntitySelect={handleEntitySelect}
          onSearch={handleSearch}
          onFilterType={handleFilterType}
          onLoadSeedData={handleLoadSeedData}
          onCreateEntity={() => setShowCreateModal(true)}
          isLoading={isLoading}
          totalEntities={totalEntities}
        />

        {/* Center: Graph Canvas */}
        <GraphWorkspace
          graphData={graphData}
          onNodeSelect={handleEntitySelect}
          selectedNodeId={selectedEntityId}
          highlightedPath={highlightedPath}
        />

        {/* Right: Entity Dossier */}
        {selectedEntityId && (
          <EntityDossier
            entityId={selectedEntityId}
            allEntities={entities}
            onClose={() => setSelectedEntityId(null)}
            onFindPath={handleFindPath}
            onFocusEntity={handleEntitySelect}
          />
        )}
      </div>

      {/* Create Entity Modal */}
      <CreateEntityModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onCreated={refreshAll}
      />
    </div>
  );
}
