// src/components/UploadForm.tsx
import { useState } from 'react';
import API from '../api/client';

export default function UploadForm() {
  const [file, setFile] = useState<File | null>(null);
  const [schemaVersion, setSchemaVersion] = useState('v1.0');
  const [msg, setMsg] = useState<string>('');

  const submit = async () => {
    if (!file) return;

    // Read & parse the file 
    let chunks: any;
    try {
      const text = await file.text();
      chunks = JSON.parse(text);
      if (!Array.isArray(chunks)) {
        throw new Error("JSON must be an array");
      }
    } catch (e: any) {
      setMsg(`Invalid JSON: ${e.message}`);
      return;
    }

    // Build the payload your API expects
    const payload = {
      schema_version: schemaVersion, // users can override if needed
      chunks: chunks                 // the array you just parsed
    };

    // 3. Send it
    try {
      const resp = await API.put('/api/upload', payload);
      setMsg(`Uploaded ${resp.data.upserted_count} chunks`);
    } catch (e: any) {
      setMsg(`Error: ${e.response?.data?.detail || e.message}`);
    }
  };

  return (
    <div style={{ margin: '20px 0' }}>
      <label>
        Schema Version:{' '}
        <input
          type="text"
          value={schemaVersion}
          onChange={e => setSchemaVersion(e.target.value)}
          style={{ width: 80 }}
        />
      </label>

      <input
        type="file"
        accept=".json"
        onChange={e => setFile(e.target.files?.[0] ?? null)}
        style={{ marginLeft: 8 }}
      />

      <button
        onClick={submit}
        disabled={!file}
        style={{ marginLeft: 8, padding: '4px 12px' }}
      >
        Upload JSON
      </button>

      {msg && <p>{msg}</p>}
    </div>
  );
}
