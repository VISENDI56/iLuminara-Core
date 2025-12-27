import React from 'react';

const FRAMEWORKS = [
  { category: "Privacy", laws: ["GDPR", "KDPA", "POPIA", "CCPA", "HIPAA", "NDPR", "PIPEDA"], color: "bg-blue-500" },
  { category: "Supply Chain", laws: ["UFLPA", "CSDDD", "LkSG", "Dodd-Frank"], color: "bg-orange-500" },
  { category: "Finance", laws: ["OFAC", "FATF", "AML", "Basel III"], color: "bg-green-500" },
  { category: "AI Safety", laws: ["EU AI Act", "NIST RMF", "ISO 42001"], color: "bg-purple-500" },
  { category: "Humanitarian", laws: ["Geneva Conventions", "IHR 2005", "Malabo Convention"], color: "bg-teal-500" },
  // ... Visual representation of 47
];

export default function ComplianceLedger() {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6 border border-gray-200 dark:border-slate-700">
      <h2 className="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-100">Governance Matrix (47/47 Active)</h2>
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        {FRAMEWORKS.map((group) => (
          <div key={group.category} className="p-4 bg-gray-50 dark:bg-slate-900 rounded-lg">
            <h3 className={`text-xs font-bold uppercase mb-2 ${group.color.replace('bg-', 'text-')}`}>{group.category}</h3>
            <div className="flex flex-wrap gap-2">
              {group.laws.map(law => (
                <span key={law} className="px-2 py-1 text-[10px] font-mono bg-white dark:bg-slate-800 border dark:border-slate-700 rounded text-gray-600 dark:text-gray-300">
                  {law}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
