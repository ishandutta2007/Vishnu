/**
 * Project Vishnu — Graph Workspace Component
 *
 * The core graph visualization canvas powered by Cytoscape.js.
 * Renders entities as nodes and relationships as edges with
 * intelligence-themed styling (color-coded by entity type).
 */
import { useEffect, useRef, useCallback } from 'react';
import cytoscape, { Core, EventObject } from 'cytoscape';
import type { GraphData } from '../types';

// ── Entity type → color mapping ─────────────────────────────────────────────
const ENTITY_COLORS: Record<string, string> = {
  person: '#38bdf8',
  organization: '#a78bfa',
  location: '#34d399',
  vehicle: '#fb923c',
  event: '#f472b6',
  document: '#94a3b8',
};

// ── Entity type → shape mapping ─────────────────────────────────────────────
const ENTITY_SHAPES: Record<string, string> = {
  person: 'ellipse',
  organization: 'round-rectangle',
  location: 'diamond',
  vehicle: 'triangle',
  event: 'star',
  document: 'rectangle',
};

interface GraphWorkspaceProps {
  graphData: GraphData | null;
  onNodeSelect: (nodeId: string) => void;
  selectedNodeId: string | null;
  highlightedPath: string[];
}

export default function GraphWorkspace({
  graphData,
  onNodeSelect,
  selectedNodeId,
  highlightedPath,
}: GraphWorkspaceProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<Core | null>(null);

  // ── Initialize Cytoscape ────────────────────────────────────────────────
  useEffect(() => {
    if (!containerRef.current) return;

    const cy = cytoscape({
      container: containerRef.current,
      style: [
        // Default node style
        {
          selector: 'node',
          style: {
            label: 'data(label)',
            'text-valign': 'bottom',
            'text-halign': 'center',
            'font-size': '11px',
            'font-family': 'Inter, sans-serif',
            color: '#cbd5e1',
            'text-margin-y': 8,
            'background-color': '#475569',
            width: 40,
            height: 40,
            'border-width': 2,
            'border-color': '#64748b',
            'text-max-width': '100px',
            'text-wrap': 'ellipsis',
          },
        },
        // Color nodes by entity type
        ...Object.entries(ENTITY_COLORS).map(([type, color]) => ({
          selector: `node[entity_type = "${type}"]`,
          style: {
            'background-color': color,
            'border-color': color,
            shape: ENTITY_SHAPES[type] || 'ellipse',
          } as any,
        })),
        // Selected node
        {
          selector: 'node:selected',
          style: {
            'border-width': 4,
            'border-color': '#fbbf24',
            width: 50,
            height: 50,
            'font-weight': 'bold' as const,
            color: '#fbbf24',
          },
        },
        // Highlighted node (path)
        {
          selector: 'node.highlighted',
          style: {
            'border-width': 4,
            'border-color': '#f97316',
            'background-opacity': 1,
          },
        },
        // Default edge style
        {
          selector: 'edge',
          style: {
            width: 1.5,
            'line-color': '#475569',
            'target-arrow-color': '#475569',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            label: 'data(label)',
            'font-size': '9px',
            'font-family': 'Inter, sans-serif',
            color: '#64748b',
            'text-rotation': 'autorotate',
            'text-margin-y': -10,
            'text-opacity': 0.7,
          },
        },
        // Highlighted edge (path)
        {
          selector: 'edge.highlighted',
          style: {
            width: 3,
            'line-color': '#f97316',
            'target-arrow-color': '#f97316',
          },
        },
        // Dimmed elements
        {
          selector: '.dimmed',
          style: {
            opacity: 0.2,
          },
        },
      ],
      layout: { name: 'cose', animate: true, animationDuration: 800 } as any,
      minZoom: 0.1,
      maxZoom: 5,
      wheelSensitivity: 0.3,
    });

    cyRef.current = cy;

    // Node click handler
    cy.on('tap', 'node', (evt: EventObject) => {
      const nodeId = evt.target.id();
      onNodeSelect(nodeId);
    });

    // Click on background to deselect
    cy.on('tap', (evt: EventObject) => {
      if (evt.target === cy) {
        onNodeSelect('');
      }
    });

    return () => {
      cy.destroy();
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // ── Update graph data ───────────────────────────────────────────────────
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy || !graphData) return;

    cy.elements().remove();

    const elements: cytoscape.ElementDefinition[] = [
      ...graphData.nodes.map((n) => ({
        group: 'nodes' as const,
        data: { ...n.data },
      })),
      ...graphData.edges.map((e) => ({
        group: 'edges' as const,
        data: { ...e.data },
      })),
    ];

    cy.add(elements);

    // Run layout
    cy.layout({
      name: 'cose',
      animate: true,
      animationDuration: 1000,
      nodeRepulsion: () => 8000,
      idealEdgeLength: () => 120,
      gravity: 0.3,
      numIter: 500,
      padding: 50,
    } as any).run();
  }, [graphData]);

  // ── Highlight selected node ─────────────────────────────────────────────
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;

    // Clear previous selection visual
    cy.elements().removeClass('dimmed');
    cy.nodes().unselect();

    if (selectedNodeId) {
      const node = cy.getElementById(selectedNodeId);
      if (node.length) {
        node.select();
        // Dim everything except neighbors
        const neighborhood = node.neighborhood().add(node);
        cy.elements().not(neighborhood).addClass('dimmed');
        neighborhood.removeClass('dimmed');
      }
    }
  }, [selectedNodeId]);

  // ── Highlight path ──────────────────────────────────────────────────────
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;

    cy.elements().removeClass('highlighted');

    if (highlightedPath.length > 0) {
      highlightedPath.forEach((id) => {
        cy.getElementById(id).addClass('highlighted');
      });

      // Also highlight edges along the path
      for (let i = 0; i < highlightedPath.length - 1; i++) {
        const src = highlightedPath[i];
        const tgt = highlightedPath[i + 1];
        cy.edges().forEach((edge) => {
          const es = edge.data('source');
          const et = edge.data('target');
          if ((es === src && et === tgt) || (es === tgt && et === src)) {
            edge.addClass('highlighted');
          }
        });
      }
    }
  }, [highlightedPath]);

  // ── Fit graph to viewport ───────────────────────────────────────────────
  const handleFitGraph = useCallback(() => {
    cyRef.current?.fit(undefined, 50);
  }, []);

  const handleRelayout = useCallback(() => {
    cyRef.current?.layout({
      name: 'cose',
      animate: true,
      animationDuration: 800,
      nodeRepulsion: () => 8000,
      idealEdgeLength: () => 120,
      gravity: 0.3,
    } as any).run();
  }, []);

  return (
    <div className="relative flex-1 h-full">
      {/* Graph Canvas */}
      <div ref={containerRef} className="w-full h-full bg-intel-darker" />

      {/* Canvas Controls */}
      <div className="absolute bottom-4 right-4 flex flex-col gap-2">
        <button
          onClick={handleFitGraph}
          className="bg-intel-panel border border-intel-border rounded-lg p-2 hover:bg-slate-700 transition-colors text-xs text-gray-300"
          title="Fit to viewport"
        >
          ⊞ Fit
        </button>
        <button
          onClick={handleRelayout}
          className="bg-intel-panel border border-intel-border rounded-lg p-2 hover:bg-slate-700 transition-colors text-xs text-gray-300"
          title="Re-layout graph"
        >
          ↻ Layout
        </button>
        <button
          onClick={() => cyRef.current?.zoom(cyRef.current.zoom() * 1.3)}
          className="bg-intel-panel border border-intel-border rounded-lg p-2 hover:bg-slate-700 transition-colors text-xs text-gray-300"
        >
          + Zoom
        </button>
        <button
          onClick={() => cyRef.current?.zoom(cyRef.current.zoom() * 0.7)}
          className="bg-intel-panel border border-intel-border rounded-lg p-2 hover:bg-slate-700 transition-colors text-xs text-gray-300"
        >
          − Zoom
        </button>
      </div>

      {/* Legend */}
      <div className="absolute top-4 right-4 bg-intel-panel/90 backdrop-blur border border-intel-border rounded-lg p-3">
        <div className="text-xs font-semibold text-gray-400 mb-2">ENTITY TYPES</div>
        {Object.entries(ENTITY_COLORS).map(([type, color]) => (
          <div key={type} className="flex items-center gap-2 text-xs text-gray-300 mb-1">
            <div
              className="w-3 h-3 rounded-sm"
              style={{ backgroundColor: color }}
            />
            <span className="capitalize">{type}</span>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {(!graphData || graphData.nodes.length === 0) && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="text-center">
            <div className="text-6xl mb-4">🔱</div>
            <h2 className="text-xl font-semibold text-gray-400 mb-2">No Graph Data</h2>
            <p className="text-gray-500 text-sm">
              Click "Load Demo Data" in the sidebar to get started
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
