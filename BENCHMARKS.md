# iLuminara-Core Benchmarks

## Current Status
- No external benchmark submissions yet.
- Focus: Internal evaluation on health-security domain tasks (refugee logistics, clinical decision chains, supply integrity).

## SWE-bench Context
SWE-bench Verified has known limitations (micro-fixes, Python-only, static dataset). Top verified scores as of Jan 2026: ~74% (Claude 4.5 Opus).

We draw inspiration from repository-scale System-2 concepts but do not claim external scores.

## Planned Internal Benchmark
- Dataset: Simulated scenarios (e.g., "Deploy Swahili clinical agent in offline camp environment")
- Metrics: Correctness, regression avoidance, formal verification pass rate, edge compatibility.

TODO:
- Create `benchmarks/health_security_tasks.json`
- Integrate with validation workflow

