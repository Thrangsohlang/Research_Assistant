// src/components/SearchBar.tsx
import { useState } from 'react';

export type SearchProps = {
  onSearch: (query: string, k?: number, minScore?: number) => void;
};

export default function SearchBar({ onSearch }: SearchProps) {
  const [query, setQuery] = useState('');
  const [kInput, setKInput] = useState<string>('');               // blank means “no override”
  const [minScoreInput, setMinScoreInput] = useState<string>('');

  const submit = () => {
    if (!query.trim()) return;

    // Parse overrides, or leave undefined
    const k    = kInput    ? parseInt(kInput, 10) : undefined;
    const min = minScoreInput ? parseFloat(minScoreInput) : undefined;

    onSearch(query, k, min);
  };

  return (
    <div style={{ margin: '20px 0' }}>
      <input
        type="text"
        placeholder="Ask a question…"
        value={query}
        onChange={e => setQuery(e.target.value)}
        style={{ width: '40%', padding: 8 }}
      />

      <input
        type="number"
        placeholder="k (opt)"
        value={kInput}
        onChange={e => setKInput(e.target.value)}
        style={{ width: 80, marginLeft: 8 }}
        min={1}
      />

      <input
        type="number"
        placeholder="min_score (opt)"
        value={minScoreInput}
        onChange={e => setMinScoreInput(e.target.value)}
        style={{ width: 100, marginLeft: 8 }}
        step={0.05}
        min={0}
        max={1}
      />

      <button onClick={submit} style={{ marginLeft: 8, padding: '8px 16px' }}>
        Search
      </button>
    </div>
  );
}
