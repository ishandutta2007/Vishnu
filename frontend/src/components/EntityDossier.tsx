/**
 * Project Vishnu — Entity Dossier Panel
 *
 * 360-degree entity profile view showing properties, relationships,
 * and quick actions (like "find shortest path").
 */
import { useEffect, useState } from 'react';
import { api } from '../api';
import type { EntityDetail, Entity } from '../types';

const ENTITY_ICONS: Record<string, string> = {
  person: '👤',
  organization: '🏢',
  location: '📍',
  vehicle: '🚗',
  event: '📅',
  document: '📄',
};

interface EntityDossierProps {
  entityId: string;
  allEntities: Entity[];
  onClose: () => void;
  onFindPath: (sourceId: string, targetId: string) => void;
  onFocusEntity: (id: string) => void;
}

export default function EntityDossier({
  entityId,
  allEntities,
  onClose,
  onFindPath,
  onFocusEntity,
}: EntityDossierProps) {
  const [entity, setEntity] = useState<EntityDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [pathTarget, setPathTarget] = useState('');

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    api.getEntity(entityId).then((data) => {
      if (!cancelled) {
        setEntity(data);
        setLoading(false);
      }
    }).catch(() => {
      if (!cancelled) setLoading(false);
    });
    return () => { cancelled = true; };
  }, [entityId]);

  if (loading) {
    return (
      <div className="w-96 bg-intel-dark border-l border-intel-border p-4 flex items-center justify-center">
        <div className="animate-spin text-2xl">⟳</div>
      </div>
    );
  }

  if (!entity) {
    return (
      <div className="w-96 bg-intel-dark border-l border-intel-border p-4 text-center text-gray-500">
        Entity not found
      </div>
    );
  }

  const classificationClass = `badge-${entity.classification_level.toLowerCase()}`;
  const entityName = (id: string) => allEntities.find((e) => e.id === id)?.name || id.slice(0, 8);

  return (
    <div className="w-96 bg-intel-dark border-l border-intel-border flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-intel-border">
        <div className="flex items-center justify-between mb-2">
          <span className={`${classificationClass} text-[10px] px-2 py-0.5 rounded font-mono`}>
            {entity.classification_level}
          </span>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-300 text-lg"
          >
            ✕
          </button>
        </div>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-2xl">{ENTITY_ICONS[entity.entity_type] || '❓'}</span>
          <div>
            <h2 className="text-lg font-semibold text-gray-100">{entity.name}</h2>
            <span className="text-xs text-gray-500 uppercase">{entity.entity_type}</span>
          </div>
        </div>
        <p className="text-sm text-gray-400 mt-2">{entity.description}</p>
      </div>

      {/* Body - Scrollable */}
      <div className="flex-1 overflow-y-auto">
        {/* Confidence & Metadata */}
        <div className="p-4 border-b border-intel-border/50">
          <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">Metadata</h3>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div>
              <span className="text-gray-500">Confidence</span>
              <div className="flex items-center gap-2 mt-1">
                <div className="flex-1 h-1.5 bg-intel-panel rounded-full">
                  <div
                    className="h-1.5 rounded-full bg-intel-accent"
                    style={{ width: `${entity.confidence_score * 100}%` }}
                  />
                </div>
                <span className="text-gray-300 font-mono">
                  {(entity.confidence_score * 100).toFixed(0)}%
                </span>
              </div>
            </div>
            <div>
              <span className="text-gray-500">Source</span>
              <div className="text-gray-300 mt-1 font-mono">{entity.source}</div>
            </div>
          </div>
          {entity.tags.length > 0 && (
            <div className="mt-3">
              <span className="text-gray-500 text-xs">Tags</span>
              <div className="flex flex-wrap gap-1 mt-1">
                {entity.tags.map((tag) => (
                  <span
                    key={tag}
                    className="bg-vishnu-900/40 text-vishnu-300 text-[10px] px-2 py-0.5 rounded-full border border-vishnu-700/30"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Properties */}
        {Object.keys(entity.properties).length > 0 && (
          <div className="p-4 border-b border-intel-border/50">
            <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">Properties</h3>
            <div className="space-y-1.5">
              {Object.entries(entity.properties).map(([key, value]) => (
                <div key={key} className="flex justify-between text-xs">
                  <span className="text-gray-500 capitalize">{key.replace(/_/g, ' ')}</span>
                  <span className="text-gray-300 font-mono text-right max-w-[60%] truncate">
                    {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Outgoing Relationships */}
        {entity.outgoing_relationships.length > 0 && (
          <div className="p-4 border-b border-intel-border/50">
            <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">
              Outgoing Links ({entity.outgoing_relationships.length})
            </h3>
            <div className="space-y-1.5">
              {entity.outgoing_relationships.map((rel) => (
                <button
                  key={rel.id}
                  onClick={() => onFocusEntity(rel.target_entity_id)}
                  className="w-full flex items-center gap-2 text-xs p-2 rounded-lg bg-intel-panel/50 hover:bg-intel-panel transition-colors text-left"
                >
                  <span className="text-intel-accent">→</span>
                  <span className="text-gray-400 font-mono text-[10px] flex-shrink-0">
                    {rel.relationship_type}
                  </span>
                  <span className="text-gray-200 truncate">
                    {entityName(rel.target_entity_id)}
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Incoming Relationships */}
        {entity.incoming_relationships.length > 0 && (
          <div className="p-4 border-b border-intel-border/50">
            <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">
              Incoming Links ({entity.incoming_relationships.length})
            </h3>
            <div className="space-y-1.5">
              {entity.incoming_relationships.map((rel) => (
                <button
                  key={rel.id}
                  onClick={() => onFocusEntity(rel.source_entity_id)}
                  className="w-full flex items-center gap-2 text-xs p-2 rounded-lg bg-intel-panel/50 hover:bg-intel-panel transition-colors text-left"
                >
                  <span className="text-green-400">←</span>
                  <span className="text-gray-400 font-mono text-[10px] flex-shrink-0">
                    {rel.relationship_type}
                  </span>
                  <span className="text-gray-200 truncate">
                    {entityName(rel.source_entity_id)}
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Shortest Path Finder */}
        <div className="p-4">
          <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">
            🔍 Find Shortest Path
          </h3>
          <div className="flex gap-2">
            <select
              value={pathTarget}
              onChange={(e) => setPathTarget(e.target.value)}
              className="flex-1 bg-intel-darker border border-intel-border rounded-lg px-2 py-1.5 text-xs text-gray-200 focus:outline-none focus:border-intel-accent"
            >
              <option value="">Select target...</option>
              {allEntities
                .filter((e) => e.id !== entityId)
                .map((e) => (
                  <option key={e.id} value={e.id}>
                    {ENTITY_ICONS[e.entity_type]} {e.name}
                  </option>
                ))}
            </select>
            <button
              onClick={() => pathTarget && onFindPath(entityId, pathTarget)}
              disabled={!pathTarget}
              className="bg-vishnu-600 hover:bg-vishnu-500 disabled:opacity-30 disabled:cursor-not-allowed text-white text-xs px-3 py-1.5 rounded-lg transition-colors"
            >
              Find
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
