import React, { useEffect, useState } from 'react';

const AuditTrail = () => {
  const [entries, setEntries] = useState([]);

  useEffect(() => {
    fetch('/audit')
      .then(res => res.json())
      .then(setEntries);
  }, []);

  return (
    <div>
      <h2>Audit Trail</h2>
      <ul>
        {entries.map((entry, i) => (
          <li key={i}>
            [{entry.timestamp}] <strong>{entry.action}</strong> by <em>{entry.user}</em> (log_id: {entry.log_id})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AuditTrail;

