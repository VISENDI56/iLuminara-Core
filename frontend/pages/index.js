import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Sidebar from '../components/Sidebar';
import LiveFeed from '../components/LiveFeed';
import ComplianceLedger from '../components/ComplianceLedger';
import System2Visualizer from '../components/System2Visualizer';

export default function CommandDashboard() {
  const [darkMode, setDarkMode] = useState(true);

  return (
    <div className={darkMode ? "dark" : ""}>
      <div className="min-h-screen bg-gray-100 dark:bg-slate-900 text-gray-900 dark:text-white transition-colors duration-300 flex">
        <Head>
          <title>iLuminara COMMAND | Sovereign Edge</title>
        </Head>
        {/* Navigation */}
        <Sidebar toggleTheme={() => setDarkMode(!darkMode)} isDark={darkMode} />
        {/* Main Content: War Room */}
        <main className="flex-1 p-6 grid grid-cols-12 gap-6">
          {/* Header */}
          <div className="col-span-12 flex justify-between items-center mb-4">
            <div>
              <h1 className="text-3xl font-bold tracking-tight text-teal-600 dark:text-teal-400">
                COMMAND DASHBOARD
              </h1>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                NODE: TensorSwitch-Edge-01 | STATUS: <span className="text-green-500 font-mono">ONLINE</span>
              </p>
            </div>
            <div className="px-4 py-2 bg-slate-200 dark:bg-slate-800 rounded-lg font-mono text-xs">
              OMNI-LAW MATRIX: 47/47 ACTIVE
            </div>
          </div>
          {/* Left Panel: System 2 Thinking */}
          <div className="col-span-12 lg:col-span-4">
            <System2Visualizer />
          </div>
          {/* Center Panel: Live Omni-Law Feed */}
          <div className="col-span-12 lg:col-span-8">
            <LiveFeed />
          </div>
          {/* Bottom Panel: Governance Ledger */}
          <div className="col-span-12">
            <ComplianceLedger />
          </div>
        </main>
      </div>
    </div>
  );
}
