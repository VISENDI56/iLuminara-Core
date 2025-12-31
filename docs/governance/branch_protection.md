# Branch Protection Policy

To maintain **ISO 42001 Integrity**, the `main` branch is protected.

## Rules of Engagement
1. **Require Signed Commits:** All commits must carry a verified GPG signature. Unsigned code is rejected.
2. **Require Pull Request Reviews:** Minimum 1 reviewer required for all merges.
3. **No Force Pushes:** History rewriting is blocked to preserve the audit trail.
4. **Status Checks:** `make stress-test` (Ghost-Nexus) must PASS before merge.

## Admin Override
Only the `Sovereign_Architect` (Founder) can bypass these rules during a declared "Code Red" emergency.