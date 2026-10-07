/**
 * Project Vishnu — Sidebar Component
 *
 * Left sidebar with entity list, search, filtering, and quick actions.
 */
import { useState } from 'react';
import type { Entity, EntityType } from '../types';

const ENTITY_ICONS: Record<string, string> = {
  person: '👤',
  organization: '🏢',
  location: '📍',
  vehicle: '🚗',
  event: '📅',
  document: '📄',
};

const ENTITY_TYPE_OPTIONS: EntityType[] = [
  'person', 'organization', 'location', 'vehicle', 'event', 'document',
];

interface SidebarProps {
  entities: Entity[];
  selectedEntityId: string | null;
  onEntitySelect: (id: string) => void;
  onSearch: (query: string) => void;
  onFilterType: (type: string | null) => void;
  onLoadSeedData: () => void;
  onCreateEntity: () => void;
  isLoading: boolean;
  totalEntities: number;
}

export default function Sidebar({
  entities,
  selectedEntityId,
  onEntitySelect,
  onSearch,
  onFilterType,
  onLoadSeedData,
  onCreateEntity,
  isLoading,
  totalEntities,
}: SidebarProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeFilter, setActiveFilter] = useState<string | null>(null);

  const handleSearch = (value: string) => {
    setSearchQuery(value);
    onSearch(value);
  };

  const handleFilterClick = (type: string) => {
    if (activeFilter === type) {
      setActiveFilter(null);
      onFilterType(null);
    } else {
      setActiveFilter(type);
      onFilterType(type);
    }
  };

  const getClassificationBadge = (level: string) => {
    const cls = `badge-${level.toLowerCase()}`;
    return (
      <span className={`${cls} text-[10px] px-1.5 py-0.5 rounded font-mono`}>
        {level}
      </span>
    );
  };

  return (
    <div className="w-80 bg-intel-dark border-r border-intel-border flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-intel-border">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">
            Entities
          </h2>
          <span className="text-xs text-gray-500 font-mono">{totalEntities} total</span>
        </div>

        {/* Search */}
        <div className="relative">
          <input
            type="text"
            placeholder="Search entities..."
            value={searchQuery}
            onChange={(e) => handleSearch(e.target.value)}
            className="w-full bg-intel-darker border border-intel-border rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-intel-accent focus:ring-1 focus:ring-intel-accent/30"
          />
          {searchQuery && (
            <button
              onClick={() => handleSearch('')}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {/* Type Filters */}
      <div className="p-3 border-b border-intel-border">
        <div className="flex flex-wrap gap-1.5">
          {ENTITY_TYPE_OPTIONS.map((type) => (
            <button
              key={type}
              onClick={() => handleFilterClick(type)}
              className={`text-xs px-2 py-1 rounded-md border transition-colors ${
                activeFilter === type
                  ? 'bg-vishnu-600/30 border-vishnu-500 text-vishnu-300'
                  : 'bg-intel-panel border-intel-border text-gray-400 hover:text-gray-200 hover:border-gray-500'
              }`}
            >
              {ENTITY_ICONS[type]} {type}
            </button>
          ))}
        </div>
      </div>

      {/* Entity List */}
      <div className="flex-1 overflow-y-auto">
        {isLoading ? (
          <div className="flex items-center justify-center h-32 text-gray-500">
            <div className="animate-spin mr-2">⟳</div> Loading...
          </div>
        ) : entities.length === 0 ? (
          <div className="p-6 text-center">
            <div className="text-4xl mb-3">📭</div>
            <p className="text-gray-500 text-sm mb-4">No entities found</p>
            <button
              onClick={onLoadSeedData}
              className="bg-vishnu-600 hover:bg-vishnu-500 text-white text-sm px-4 py-2 rounded-lg transition-colors glow-pulse"
            >
              🚀 Load Demo Data
            </button>
          </div>
        ) : (
          entities.map((entity) => (
            <button
              key={entity.id}
              onClick={() => onEntitySelect(entity.id)}
              className={`w-full text-left p-3 border-b border-intel-border/50 hover:bg-intel-panel/50 transition-colors ${
                selectedEntityId === entity.id ? 'bg-intel-panel border-l-2 border-l-intel-accent' : ''
              }`}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-1.5 mb-1">
                    <span className="text-base">{ENTITY_ICONS[entity.entity_type] || '❓'}</span>
                    <span className="text-sm font-medium text-gray-200 truncate">
                      {entity.name}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 line-clamp-2">
                    {entity.description || 'No description'}
                  </p>
                </div>
                <div className="flex flex-col items-end gap-1 flex-shrink-0">
                  {getClassificationBadge(entity.classification_level)}
                  <span className="text-[10px] text-gray-600 font-mono">
                    {(entity.confidence_score * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            </button>
          ))
        )}
      </div>

      {/* Bottom Actions */}
      <div className="p-3 border-t border-intel-border flex gap-2">
        <button
          onClick={onLoadSeedData}
          className="flex-1 bg-intel-panel border border-intel-border text-gray-300 text-xs px-3 py-2 rounded-lg hover:bg-slate-700 transition-colors"
        >
          🗃️ Load Demo
        </button>
        <button
          onClick={onCreateEntity}
          className="flex-1 bg-vishnu-600 hover:bg-vishnu-500 text-white text-xs px-3 py-2 rounded-lg transition-colors"
        >
          + New Entity
        </button>
      </div>
    </div>
  );
}
