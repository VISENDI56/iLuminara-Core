import React, { useEffect, useState } from 'react';

export default function LiveFeed() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    // Connect to Python Backend
    const ws = new WebSocket('ws://localhost:8000/ws/live-feed');
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLogs((prev) => [data, ...prev].slice(0, 7)); // Keep last 7 items
    };
    return () => ws.close();
  }, []);

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6 border border-gray-200 dark:border-slate-700 h-full">
      <h2 className="text-lg font-semibold mb-4 flex items-center">
        <span className="animate-pulse h-3 w-3 bg-red-500 rounded-full mr-2"></span>
        Real-Time Omni-Law Intercepts
      </h2>
      <div className="space-y-3">
        {logs.map((log, idx) => (
          <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-slate-900 rounded-md border-l-4"
            style={{ borderColor: log.result.status === 'BLOCKED' ? '#ef4444' : '#22c55e' }}>
            <div className="flex flex-col">
              <span className="text-xs font-bold uppercase text-gray-500 tracking-wider">{log.sector}</span>
              <span className="text-sm font-medium">{log.result.status}</span>
            </div>
            <div className="text-xs text-right font-mono text-gray-400">
              {JSON.stringify(log.data).slice(0, 30)}...
            </div>
          </div>
        ))}
        {logs.length === 0 && <p className="text-center text-gray-500 mt-10">Connecting to Sovereign Edge...</p>}
      </div>
    </div>
  );
}
