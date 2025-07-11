import { useState, useEffect } from 'react';
import API from '../api/client';

const TOKEN_KEY = 'access_token';

export default function TokenPanel() {
  // Read initial value from localStorage
  const [token, setToken] = useState<string>(() => {
    return localStorage.getItem(TOKEN_KEY) || '';
  });
  const [input, setInput] = useState(token);

  // Keep localStorage & Axios interceptor in sync
  useEffect(() => {
    if (token) {
      localStorage.setItem(TOKEN_KEY, token);
    } else {
      localStorage.removeItem(TOKEN_KEY);
    }
  }, [token]);

  const save = () => {
    setToken(input.trim());
  };
  const clear = () => {
    setToken('');
    setInput('');
  };

  return (
    <div style={{
      border: '1px solid #ccc',
      padding: 12,
      marginBottom: 16,
      borderRadius: 4,
      fontFamily: 'sans-serif',
      background: '#fafafa'
    }}>
      <strong>API Token</strong>
      <div style={{ marginTop: 8, display: 'flex', alignItems: 'center' }}>
        <input
          type="text"
          placeholder="Paste your Bearer token here"
          value={input}
          onChange={e => setInput(e.target.value)}
          style={{ flex: 1, padding: 6, fontFamily: 'monospace' }}
        />
        <button onClick={save} style={{ marginLeft: 8, padding: '6px 12px' }}>
          Save
        </button>
        <button onClick={clear} style={{ marginLeft: 4, padding: '6px 12px' }}>
          Clear
        </button>
      </div>
      {token && (
        <div style={{ marginTop: 8, fontSize: 12, color: '#555' }}>
          Current token: <code style={{ display: 'inline-block', maxWidth: 400, overflowX: 'auto' }}>{token}</code>
        </div>
      )}
      {!token && (
        <div style={{ marginTop: 8, fontSize: 12, color: 'red' }}>
          No token set—API calls will be unauthorized.
        </div>
      )}
    </div>
  );
}
