/**
 * Project Vishnu — Create Entity Modal
 *
 * Form modal for creating new entities.
 */
import { useState } from 'react';
import { api } from '../api';
import type { EntityType, ClassificationLevel } from '../types';

const ENTITY_TYPES: EntityType[] = [
  'person', 'organization', 'location', 'vehicle', 'event', 'document',
];

const CLASSIFICATION_LEVELS: ClassificationLevel[] = [
  'UNCLASSIFIED', 'RESTRICTED', 'CONFIDENTIAL', 'SECRET', 'TOP_SECRET',
];

interface CreateEntityModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreated: () => void;
}

export default function CreateEntityModal({ isOpen, onClose, onCreated }: CreateEntityModalProps) {
  const [entityType, setEntityType] = useState<EntityType>('person');
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [classification, setClassification] = useState<ClassificationLevel>('UNCLASSIFIED');
  const [confidence, setConfidence] = useState(1.0);
  const [tags, setTags] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setError('Name is required');
      return;
    }

    setSubmitting(true);
    setError('');

    try {
      await api.createEntity({
        entity_type: entityType,
        name: name.trim(),
        description: description.trim(),
        classification_level: classification,
        confidence_score: confidence,
        tags: tags.split(',').map((t) => t.trim()).filter(Boolean),
      });
      onCreated();
      // Reset form
      setName('');
      setDescription('');
      setTags('');
      setConfidence(1.0);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create entity');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-intel-dark border border-intel-border rounded-xl shadow-2xl w-full max-w-lg mx-4">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-intel-border">
          <h2 className="text-lg font-semibold text-gray-100">Create New Entity</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-300 text-lg">
            ✕
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {/* Entity Type */}
          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase mb-1.5">
              Entity Type
            </label>
            <div className="flex flex-wrap gap-2">
              {ENTITY_TYPES.map((type) => (
                <button
                  key={type}
                  type="button"
                  onClick={() => setEntityType(type)}
                  className={`text-xs px-3 py-1.5 rounded-lg border transition-colors capitalize ${
                    entityType === type
                      ? 'bg-vishnu-600/30 border-vishnu-500 text-vishnu-300'
                      : 'bg-intel-panel border-intel-border text-gray-400 hover:text-gray-200'
                  }`}
                >
                  {type}
                </button>
              ))}
            </div>
          </div>

          {/* Name */}
          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase mb-1.5">
              Name *
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g., Viktor Sorokin"
              className="w-full bg-intel-darker border border-intel-border rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-intel-accent"
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase mb-1.5">
              Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Intelligence summary..."
              rows={3}
              className="w-full bg-intel-darker border border-intel-border rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-intel-accent resize-none"
            />
          </div>

          {/* Classification & Confidence */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-gray-400 uppercase mb-1.5">
                Classification
              </label>
              <select
                value={classification}
                onChange={(e) => setClassification(e.target.value as ClassificationLevel)}
                className="w-full bg-intel-darker border border-intel-border rounded-lg px-3 py-2 text-sm text-gray-200 focus:outline-none focus:border-intel-accent"
              >
                {CLASSIFICATION_LEVELS.map((level) => (
                  <option key={level} value={level}>{level}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-gray-400 uppercase mb-1.5">
                Confidence ({(confidence * 100).toFixed(0)}%)
              </label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={confidence}
                onChange={(e) => setConfidence(parseFloat(e.target.value))}
                className="w-full mt-2"
              />
            </div>
          </div>

          {/* Tags */}
          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase mb-1.5">
              Tags (comma-separated)
            </label>
            <input
              type="text"
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              placeholder="e.g., HVT, financier, nightfall"
              className="w-full bg-intel-darker border border-intel-border rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-intel-accent"
            />
          </div>

          {/* Error */}
          {error && (
            <div className="bg-red-900/30 border border-red-700 text-red-300 text-xs px-3 py-2 rounded-lg">
              {error}
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="text-gray-400 hover:text-gray-200 text-sm px-4 py-2 rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="bg-vishnu-600 hover:bg-vishnu-500 disabled:opacity-50 text-white text-sm px-6 py-2 rounded-lg transition-colors"
            >
              {submitting ? 'Creating...' : 'Create Entity'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
