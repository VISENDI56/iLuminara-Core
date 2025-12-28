import React from 'react';

export default function System2Visualizer() {
  return (
    <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl shadow-lg p-6 text-white h-full relative overflow-hidden border border-slate-700">
      <div className="absolute top-0 right-0 p-2 opacity-10">
        <svg className="w-24 h-24" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a8 8 0 100 16 8 8 0 000-16z" /></svg>
      </div>
      <h2 className="text-lg font-semibold mb-6 flex items-center">
        <span className="text-teal-400 mr-2">◈</span> System 2 Agent
      </h2>
      <div className="space-y-6 relative z-10">
        {/* Step 1: Plan */}
        <div className="flex items-start opacity-50 hover:opacity-100 transition-opacity">
          <div className="flex-shrink-0 h-6 w-6 rounded-full bg-teal-900 flex items-center justify-center border border-teal-500 text-xs">1</div>
          <div className="ml-4">
            <h4 className="text-sm font-bold text-teal-400">Planning</h4>
            <p className="text-xs text-slate-400">Generating Specification...</p>
          </div>
        </div>
        {/* Step 2: Simulate */}
        <div className="flex items-start opacity-100 scale-105 transition-transform">
          <div className="flex-shrink-0 h-6 w-6 rounded-full bg-blue-900 flex items-center justify-center border border-blue-500 text-xs animate-pulse">2</div>
          <div className="ml-4">
            <h4 className="text-sm font-bold text-blue-400">Simulation</h4>
            <p className="text-xs text-slate-300">Running Causal Twin (Sandboxed)</p>
            <div className="mt-1 h-1 w-full bg-slate-700 rounded-full overflow-hidden">
              <div className="h-full bg-blue-500 w-2/3 animate-[loading_1s_ease-in-out_infinite]"></div>
            </div>
          </div>
        </div>
        {/* Step 3: Validate */}
        <div className="flex items-start opacity-50">
          <div className="flex-shrink-0 h-6 w-6 rounded-full bg-slate-800 flex items-center justify-center border border-slate-600 text-xs">3</div>
          <div className="ml-4">
            <h4 className="text-sm font-bold text-slate-400">Execution</h4>
            <p className="text-xs text-slate-500">Waiting for validation...</p>
          </div>
        </div>
      </div>
    </div>
  );
}
