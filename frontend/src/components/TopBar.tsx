/**
 * Project Vishnu — Top Bar Component
 *
 * Application header with branding, global search, and analytics quick-access.
 */
import { useState } from 'react';
import type { CentralityResult, Community } from '../types';

interface TopBarProps {
  onGlobalSearch: (query: string) => void;
  onShowCentrality: () => void;
  onShowCommunities: () => void;
  centralityResults: CentralityResult[];
  communityResults: Community[];
  showAnalytics: 'centrality' | 'communities' | null;
  onCloseAnalytics: () => void;
  onFocusEntity: (id: string) => void;
}

export default function TopBar({
  onGlobalSearch,
  onShowCentrality,
  onShowCommunities,
  centralityResults,
  communityResults,
  showAnalytics,
  onCloseAnalytics,
  onFocusEntity,
}: TopBarProps) {
  const [searchValue, setSearchValue] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchValue.trim()) onGlobalSearch(searchValue.trim());
  };

  return (
    <>
      <header className="bg-intel-dark border-b border-intel-border px-4 py-2 flex items-center justify-between flex-shrink-0">
        {/* Logo & Title */}
        <div className="flex items-center gap-3">
          <span className="text-2xl">🔱</span>
          <div>
            <h1 className="text-base font-bold text-gray-100 leading-tight">
              VISHNU
            </h1>
            <span className="text-[10px] text-gray-500 uppercase tracking-widest">
              openGotham Intelligence Platform
            </span>
          </div>
        </div>

        {/* Global Search */}
        <form onSubmit={handleSearch} className="flex-1 max-w-xl mx-8">
          <div className="relative">
            <input
              type="text"
              placeholder="Global search across all entities..."
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
              className="w-full bg-intel-darker border border-intel-border rounded-lg px-4 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-intel-accent focus:ring-1 focus:ring-intel-accent/30"
            />
            <button
              type="submit"
              className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-intel-accent text-sm"
            >
              🔍
            </button>
          </div>
        </form>

        {/* Analytics Buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={onShowCentrality}
            className="bg-intel-panel border border-intel-border text-gray-300 text-xs px-3 py-1.5 rounded-lg hover:bg-slate-700 hover:text-intel-accent transition-colors"
          >
            📊 Key Nodes
          </button>
          <button
            onClick={onShowCommunities}
            className="bg-intel-panel border border-intel-border text-gray-300 text-xs px-3 py-1.5 rounded-lg hover:bg-slate-700 hover:text-intel-accent transition-colors"
          >
            🧩 Communities
          </button>
          <div className="w-px h-6 bg-intel-border mx-1" />
          <span className="text-xs text-gray-600 font-mono">v0.1.0</span>
        </div>
      </header>

      {/* Analytics Panel (slides down) */}
      {showAnalytics && (
        <div className="bg-intel-dark border-b border-intel-border px-4 py-3 flex-shrink-0">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-semibold text-gray-300">
              {showAnalytics === 'centrality' ? '📊 Key Nodes (Betweenness Centrality)' : '🧩 Detected Communities'}
            </h3>
            <button onClick={onCloseAnalytics} className="text-gray-500 hover:text-gray-300">
              ✕
            </button>
          </div>

          {showAnalytics === 'centrality' && (
            <div className="flex flex-wrap gap-2">
              {centralityResults.map((r, i) => (
                <button
                  key={r.id}
                  onClick={() => onFocusEntity(r.id)}
                  className="bg-intel-panel border border-intel-border rounded-lg px-3 py-1.5 text-xs hover:border-intel-accent transition-colors flex items-center gap-2"
                >
                  <span className="text-yellow-400 font-bold">#{i + 1}</span>
                  <span className="text-gray-200">{r.label}</span>
                  <span className="text-gray-500 font-mono">
                    ({(r.centrality_score * 100).toFixed(1)}%)
                  </span>
                </button>
              ))}
              {centralityResults.length === 0 && (
                <span className="text-gray-500 text-xs">No data — load some entities first</span>
              )}
            </div>
          )}

          {showAnalytics === 'communities' && (
            <div className="flex flex-wrap gap-3">
              {communityResults.map((c) => (
                <div
                  key={c.community_id}
                  className="bg-intel-panel border border-intel-border rounded-lg p-2"
                >
                  <div className="text-xs font-semibold text-gray-400 mb-1">
                    Community {c.community_id + 1} ({c.size} members)
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {c.members.map((m) => (
                      <button
                        key={m.id}
                        onClick={() => onFocusEntity(m.id)}
                        className="text-[10px] bg-intel-darker px-2 py-0.5 rounded text-gray-300 hover:text-intel-accent transition-colors"
                      >
                        {m.label}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
              {communityResults.length === 0 && (
                <span className="text-gray-500 text-xs">No data — load some entities first</span>
              )}
            </div>
          )}
        </div>
      )}
    </>
  );
}
