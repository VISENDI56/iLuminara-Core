import React from 'react';

export default function Sidebar({ toggleTheme, isDark }) {
  return (
    <div className="w-64 bg-white dark:bg-slate-800 border-r border-gray-200 dark:border-slate-700 p-4">
      <h2 className="text-lg font-bold mb-4 text-teal-600 dark:text-teal-400">iLuminara</h2>
      <button
        onClick={toggleTheme}
        className="px-4 py-2 bg-gray-200 dark:bg-slate-700 rounded hover:bg-gray-300 dark:hover:bg-slate-600 transition-colors"
      >
        {isDark ? 'Light' : 'Dark'} Mode
      </button>
      <nav className="mt-6">
        <ul className="space-y-2">
          <li><a href="#" className="block px-4 py-2 rounded hover:bg-gray-100 dark:hover:bg-slate-700">Dashboard</a></li>
          <li><a href="#" className="block px-4 py-2 rounded hover:bg-gray-100 dark:hover:bg-slate-700">Compliance</a></li>
          <li><a href="#" className="block px-4 py-2 rounded hover:bg-gray-100 dark:hover:bg-slate-700">Agents</a></li>
        </ul>
      </nav>
    </div>
  );
}
