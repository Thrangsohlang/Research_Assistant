import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; // This imports the default CSS for the body, etc.
import App from './App'; // This imports your main App component

// Get the root HTML element where your React app will be mounted
const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement // 'root' is the id of a div in public/index.html
);

// Render your App component into the root
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);