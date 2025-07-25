import React, { useState } from 'react';

const LogViewer = () => {
  const [logId, setLogId] = useState('');
  const [log, setLog] = useState(null);

  const fetchLog = async () => {
    const res = await fetch(`/logs/${logId}`);
    const data = await res.json();
    setLog(data);
  };

  return (
    <div>
      <h2>View Encrypted Log</h2>
      <input value={logId} onChange={e => setLogId(e.target.value)} placeholder="Enter Log ID" />
      <button onClick={fetchLog}>Fetch Log</button>
      {log && (
        <pre>{JSON.stringify(log, null, 2)}</pre>
      )}
    </div>
  );
};

export default LogViewer;
