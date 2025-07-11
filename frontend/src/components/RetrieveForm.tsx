// src/components/RetrieveForm.tsx
import { useState } from 'react';
import API from '../api/client';

export default function RetrieveForm() {
  const [journalId, setJournalId] = useState('');
  const [doc, setDoc] = useState<any>(null);

  const fetch = async () => {
    try {
      const resp = await API.get(`/api/${journalId}`);
      setDoc(resp.data);
    } catch (e: any) {
      setDoc({ error: e.response?.data?.detail || e.message });
    }
  };

  return (
    <div style={{ margin: '20px 0' }}>
      <input
        type="text"
        placeholder="Journal ID (filename)"
        value={journalId}
        onChange={e => setJournalId(e.target.value)}
        style={{ width: '60%', padding: 8 }}
      />
      <button onClick={fetch} style={{ marginLeft: 8 }}>Load</button>
      {doc && (
        <pre style={{ maxHeight: 300, overflow: 'auto', background: '#f7f7f7', padding: 8 }}>
          {doc.error ? doc.error : JSON.stringify(doc, null, 2)}
        </pre>
      )}
    </div>
  );
}
