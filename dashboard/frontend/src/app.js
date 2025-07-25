import React from 'react';
import LogViewer from './components/LogViewer';
import AuditTrail from './components/AuditTrail';

function App() {
  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1>📜 Privacy-First Log Dashboard</h1>
      <LogViewer />
      <AuditTrail />
    </div>
  );
}

export default App;
