import { useState } from 'react';
import TokenPanel from './components/TokenPanel';
import SearchBar from './components/SearchBar';
import ResultsList, { Hit } from './components/ResultsList';
import UploadForm from './components/UploadForm';
import RetrieveForm from './components/RetrieveForm';
import API from './api/client';

function App() {
  const [hits, setHits] = useState<Hit[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (query: string, k?: number, minScore?: number) => {
    if (!query.trim()) return;
    setLoading(true);

    const payload: any = { query };
    if (k !== undefined) payload.k = k;
    if (minScore !== undefined) payload.min_score = minScore;

    try {
      const resp = await API.post('/api/similarity_search', payload);
      setHits(resp.data.results);
    } catch (err: any) {
      alert(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: '40px auto', fontFamily: 'sans-serif' }}>
      <h1>GenAI Research Assistant</h1>

      {/* Token input panel */}
      <TokenPanel />

      {/* Ingestion & retrieval */}
      <UploadForm />
      <RetrieveForm />

      {/* Search */}
      <SearchBar onSearch={handleSearch} />
      {loading ? <p>Searching…</p> : <ResultsList hits={hits} />}
    </div>
  );
}

export default App;
