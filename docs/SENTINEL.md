# Sentinel v3.0 - Sovereign DevSecOps Engine

## 🔒 Executive Summary

Sentinel v3.0 is a production-grade DevSecOps pipeline designed for the iLuminara sovereign biosecurity infrastructure. It provides automated security scanning, cryptographic integrity verification, and seamless integration with GitHub Security.

### Key Capabilities
- ✅ **Dual-Mode Operation**: BASELINE generation and SCAN verification
- ✅ **Cryptographic Integrity**: SHA-256 hashing with JSON ledger storage
- ✅ **Secret Scanning**: Detection of 6 types of hardcoded credentials
- ✅ **SAST Analysis**: Detection of 5 CWE vulnerability patterns
- ✅ **SARIF Output**: GitHub Security-compatible reporting
- ✅ **Edge Optimization**: Memory-efficient for Jetson Orin deployment

---

## 🏗️ Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                   Sentinel v3.0 Core                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Baseline   │  │   Security   │  │   Integrity  │ │
│  │  Generator   │  │   Scanner    │  │   Verifier   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│         │                 │                  │          │
│         └─────────────────┴──────────────────┘          │
│                           ▼                             │
│                   ┌──────────────┐                      │
│                   │    SARIF     │                      │
│                   │   Generator  │                      │
│                   └──────────────┘                      │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │     GitHub Security Integration       │
        ├───────────────────────────────────────┤
        │  • Security Alerts                    │
        │  • PR Comments                        │
        │  • Hard Blocking                      │
        │  • 90-Day Audit Trail                 │
        └───────────────────────────────────────┘
```

### Scanning Modes

#### BASELINE Mode
- Generates cryptographic fingerprints (SHA-256) for all tracked files
- Creates `enterprise/integrity_ledger.json` with file hashes
- Provides golden state for integrity verification
- Should be regenerated after verified code changes

#### SCAN Mode
- Compares current file hashes against baseline ledger
- Performs secret scanning for hardcoded credentials
- Executes SAST analysis for common vulnerabilities
- Generates SARIF report for GitHub Security
- Blocks deployment on critical/error findings

---

## 📋 Usage Instructions

### Prerequisites
- Python 3.10 or higher
- Git repository
- No additional dependencies required (uses stdlib only)

### Command Line Usage

#### Generate Integrity Baseline
```bash
python3 enterprise/sentinel.py --mode BASELINE
```

**Output:**
```
╔════════ SENTINEL v3.0 (BASELINE) ════════╗
   Root: /path/to/repo
   Mode: BASELINE
════════════════════════════════════════════════
   [+] Hashed 10 files...
   [+] Hashed 20 files...
...
✅ GOLDEN STATE LOCKED: 251 files hashed.
   Ledger saved to: enterprise/integrity_ledger.json
```

#### Run Security Scan
```bash
python3 enterprise/sentinel.py --mode SCAN
```

**Output (Clean System):**
```
╔════════ SENTINEL v3.0 (SCAN) ════════╗
   Root: /path/to/repo
   Mode: SCAN
════════════════════════════════════════════════

📊 SCAN COMPLETE: 251 files analyzed
✅ SYSTEM SECURE. NO THREATS DETECTED.
```

**Output (Issues Detected):**
```
╔════════ SENTINEL v3.0 (SCAN) ════════╗
   Root: /path/to/repo
   Mode: SCAN
════════════════════════════════════════════════
   [ERROR] SEC-002: Dangerous pattern: Secret: OpenAI API Key
           File: config.py:15
   [CRITICAL] INT-001: Integrity Violation: File Modified Since Baseline
           File: core/auth.py:1

📊 SCAN COMPLETE: 251 files analyzed
   🔴 Critical: 1
   🟠 Errors:   1
   🟡 Warnings: 0

❌ SECURITY GATE FAILED: 2 issues found.
```

### Exit Codes
- `0`: Success - No security issues detected
- `1`: Failure - Security issues found
- `130`: Interrupted by user (Ctrl+C)

---

## 🔍 Detection Capabilities

### Secret Scanning

Sentinel detects 6 types of hardcoded credentials:

| Rule ID | Pattern | Description |
|---------|---------|-------------|
| SEC-001 | `AIza[0-9A-Za-z-_]{35}` | Google API Key |
| SEC-002 | `sk-[a-zA-Z0-9]{32,}` | OpenAI API Key |
| SEC-003 | `AKIA[0-9A-Z]{16}` | AWS Access Key |
| SEC-004 | `-----BEGIN PRIVATE KEY-----` | Private Key (PEM) |
| SEC-005 | `ghp_[a-zA-Z0-9]{36}` | GitHub Personal Access Token |
| SEC-006 | `postgres://[^:]+:[^@]+@` | Database Connection String |

**Severity:** All secrets are flagged as `error` level.

### SAST Analysis

Detects 5 common vulnerability patterns:

| Rule ID | Pattern | CWE | Description |
|---------|---------|-----|-------------|
| CWE-95 | `eval()` | CWE-95 | Code Injection via eval |
| CWE-95 | `exec()` | CWE-95 | Code Injection via exec |
| CWE-502 | `pickle.loads` | CWE-502 | Insecure Deserialization |
| CWE-78 | `os.system()` | CWE-78 | OS Command Injection |
| CWE-78 | `subprocess.call(..., shell=True)` | CWE-78 | Shell Injection Risk |

**Severity:** SAST findings are flagged as `warning` level.

### Integrity Verification

| Rule ID | Description | Severity |
|---------|-------------|----------|
| INT-001 | File modified since baseline | critical |

---

## 🚀 CI/CD Integration

### GitHub Actions Workflow

Sentinel v3.0 is integrated via `.github/workflows/sentinel-gate.yml`:

#### Workflow Features
- ✅ Automated scanning on push/PR to main/develop branches
- ✅ SARIF upload to GitHub Security tab
- ✅ Hard blocking on critical/error findings
- ✅ PR comment feedback with security summary
- ✅ 90-day audit trail retention
- ✅ Baseline caching for performance

#### Workflow Execution
```yaml
on:
  push:
    branches: [ "main", "develop" ]
  pull_request:
    branches: [ "main", "develop" ]
```

#### Security Gate Behavior
- **Pass**: Zero critical/error findings → Deployment authorized
- **Fail**: Any critical/error findings → Deployment blocked
- **PR Comments**: Automatic security summary posted to PRs

#### Example PR Comment
```markdown
## 🔒 Sentinel v3.0 Security Scan Results

❌ **SECURITY GATE FAILED**

**Summary:**
- 🔴 Critical: 1
- 🟠 Errors: 2
- 🟡 Warnings: 3
- 📊 Total Issues: 6

**Action Required:** Please review and remediate security findings before merging.

**View Details:** Check the Security tab for full SARIF report.

---
*Powered by Sentinel v3.0 | NIST SP 800-208 Compliant*
```

### Local Development Workflow

1. **Make Code Changes**
   ```bash
   # Edit files as needed
   vim src/feature.py
   ```

2. **Run Local Scan**
   ```bash
   python3 enterprise/sentinel.py --mode SCAN
   ```

3. **Fix Any Issues**
   ```bash
   # Address security findings
   # Re-run scan until clean
   ```

4. **Update Baseline (if needed)**
   ```bash
   # Only after verifying changes are safe
   python3 enterprise/sentinel.py --mode BASELINE
   ```

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: add new feature (security verified)"
   git push origin feature-branch
   ```

6. **CI Validation**
   - Sentinel runs automatically
   - SARIF uploaded to GitHub Security
   - PR receives automated feedback

---

## 🖥️ Jetson Orin Edge Deployment

### Memory Optimization Features

Sentinel is optimized for resource-constrained edge environments:

#### File Size Limits
```python
MAX_FILE_SIZE_MB = 10  # Skip model weights and large binaries
```

**Rationale:** ML models (`.pt`, `.tflite`, `.onnx`) are skipped to prevent memory exhaustion.

#### Streaming Hash Computation
```python
def _calculate_hash(self, filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):  # 64KB chunks
            sha256.update(chunk)
    return sha256.hexdigest()
```

**Benefit:** Processes large files without loading entire contents into memory.

#### Selective Directory Pruning
```python
SKIP_DIRS = {".git", "venv", "__pycache__", "logs", "node_modules", ".venv"}
```

**Benefit:** Avoids scanning non-critical directories.

### Deployment Steps on Jetson Orin

1. **Clone Repository**
   ```bash
   git clone https://github.com/VISENDI56/iLuminara-Core.git
   cd iLuminara-Core
   ```

2. **Verify Python Installation**
   ```bash
   python3 --version  # Should be 3.10+
   ```

3. **Generate Baseline**
   ```bash
   python3 enterprise/sentinel.py --mode BASELINE
   ```

4. **Setup Automated Scanning (Optional)**
   ```bash
   # Add to cron for periodic scans
   crontab -e
   # Add line:
   0 2 * * * cd /path/to/iLuminara-Core && python3 enterprise/sentinel.py --mode SCAN >> /var/log/sentinel.log 2>&1
   ```

5. **Monitor Results**
   ```bash
   tail -f /var/log/sentinel.log
   ```

### Resource Requirements

| Resource | Requirement | Notes |
|----------|-------------|-------|
| Memory | ~50MB | For repos <1000 files |
| CPU | Minimal | Single-threaded, low overhead |
| Storage | <1MB | Ledger file + SARIF report |
| Python | 3.10+ | No external dependencies |

---

## 🛡️ Compliance Mapping

### NIST SP 800-208: Recommendation for Stateful HBS
**Section:** 4.3 - Integrity Verification of Critical Kernels

**Implementation:**
- SHA-256 cryptographic hashing of all source files
- Baseline ledger (golden state) stored in version control
- Automated verification on every deployment
- Detection of unauthorized modifications (INT-001)

**Compliance Evidence:**
```json
{
  "compliance_framework": "NIST SP 800-208",
  "control": "4.3 - Integrity Verification",
  "implementation": {
    "hash_algorithm": "SHA-256",
    "baseline_storage": "enterprise/integrity_ledger.json",
    "verification_frequency": "every_deployment",
    "audit_trail": "90_days"
  }
}
```

### NIST 800-53 CA-7: Continuous Monitoring
**Control:** CA-7 - Continuous Monitoring

**Implementation:**
- Automated security scanning on every code change
- Real-time detection of secrets and vulnerabilities
- Continuous verification against integrity baseline
- GitHub Security integration for centralized monitoring

### NIST 800-53 AU-11: Audit Record Retention
**Control:** AU-11 - Audit Record Retention

**Implementation:**
- 90-day retention of SARIF reports in GitHub Artifacts
- Persistent storage in GitHub Security tab
- Immutable audit trail via Git commit history

### CWE Top-25: Common Weakness Enumeration
**Coverage:**
- CWE-78: OS Command Injection
- CWE-95: Code Injection (eval/exec)
- CWE-502: Deserialization of Untrusted Data

---

## 🔧 Troubleshooting Guide

### Common Issues

#### Issue: "Corrupted ledger file"
**Symptom:**
```
⚠️  Warning: Corrupted ledger file at enterprise/integrity_ledger.json
```

**Solution:**
```bash
# Regenerate baseline
python3 enterprise/sentinel.py --mode BASELINE
```

#### Issue: "Cannot read file: Permission denied"
**Symptom:**
```
⚠️  Cannot read /path/to/file: Permission denied
```

**Solution:**
```bash
# Fix file permissions
chmod 644 /path/to/file

# Or skip the file by adding to SKIP_EXTS
```

#### Issue: False Positive - Pattern in Comments
**Symptom:**
```
[ERROR] SEC-002: Secret: OpenAI API Key
File: config.py:15
```

**Context:** Pattern appears in comments or test data

**Solution:**
1. Review the detection in context
2. If legitimate (e.g., documentation of pattern format), consider:
   - Moving pattern to external documentation
   - Using environment variables instead
   - Accepting the finding as expected

#### Issue: Integrity Violation After Valid Update
**Symptom:**
```
[CRITICAL] INT-001: Integrity Violation: File Modified Since Baseline
File: feature.py:1
```

**Solution:**
```bash
# After verifying changes are intentional and safe:
python3 enterprise/sentinel.py --mode BASELINE

# Commit updated ledger
git add enterprise/integrity_ledger.json
git commit -m "chore: update integrity baseline"
```

#### Issue: CI Workflow Fails but Local Scan Passes
**Possible Causes:**
1. Baseline ledger not in sync between local and CI
2. Different Python versions
3. File encoding differences

**Solution:**
```bash
# Ensure ledger is committed
git add enterprise/integrity_ledger.json
git commit -m "chore: update baseline"
git push

# Force regenerate baseline in CI by clearing cache
```

### Performance Optimization

#### Slow Scans (Large Repositories)
**Symptoms:**
- Baseline generation takes >5 minutes
- SCAN mode times out in CI

**Solutions:**
1. **Increase File Size Limit** (for repos with few large files):
   ```python
   MAX_FILE_SIZE_MB = 50  # In sentinel.py
   ```

2. **Add More Skip Patterns**:
   ```python
   SKIP_DIRS.update({"docs", "examples", "tests/fixtures"})
   SKIP_EXTS.update({".md", ".txt", ".csv"})
   ```

3. **Use Parallel Scanning** (advanced):
   ```bash
   # Split scan across multiple workers
   # (Requires custom implementation)
   ```

### Debug Mode

To enable verbose logging:

```python
# Add to sentinel.py (temporary debugging)
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📊 SARIF Output Format

Sentinel generates GitHub-compatible SARIF 2.1.0 reports:

```json
{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [{
    "tool": {
      "driver": {
        "name": "iLuminara Sentinel",
        "version": "3.0",
        "informationUri": "https://github.com/VISENDI56/iLuminara-Core"
      }
    },
    "results": [
      {
        "ruleId": "SEC-002",
        "message": {
          "text": "Dangerous pattern: Secret: OpenAI API Key"
        },
        "locations": [{
          "physicalLocation": {
            "artifactLocation": {"uri": "config.py"},
            "region": {
              "startLine": 15,
              "snippet": {"text": "api_key = \"sk-abcd1234...\""}
            }
          }
        }],
        "level": "error"
      }
    ]
  }]
}
```

### SARIF Benefits
- ✅ Native GitHub Security tab integration
- ✅ Code annotation in PR diffs
- ✅ Unified vulnerability management
- ✅ Exportable for external SIEM systems

---

## 🚦 Testing & Validation

### Test 1: Baseline Generation
```bash
python3 enterprise/sentinel.py --mode BASELINE
# Verify: enterprise/integrity_ledger.json created
cat enterprise/integrity_ledger.json | jq '. | length'
```

### Test 2: Clean Scan
```bash
python3 enterprise/sentinel.py --mode SCAN
# Expected: Exit code 0, "SYSTEM SECURE"
echo $?  # Should output: 0
```

### Test 3: Secret Detection
```bash
echo 'API_KEY="sk-test1234567890abcdef1234567890ab"' > test_secret.py
python3 enterprise/sentinel.py --mode SCAN
# Expected: SEC-002 detection, exit code 1
rm test_secret.py
```

### Test 4: Integrity Detection
```bash
echo "# tampered" >> README.md
python3 enterprise/sentinel.py --mode SCAN
# Expected: INT-001 detection, exit code 1
git checkout README.md
```

### Test 5: SARIF Generation
```bash
python3 enterprise/sentinel.py --mode SCAN
cat sentinel_report.sarif | jq '.runs[0].tool.driver.name'
# Expected: "iLuminara Sentinel"
```

---

## 📚 Additional Resources

### Related Documentation
- [GitHub Security Overview](https://docs.github.com/en/code-security)
- [SARIF Specification](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html)
- [NIST SP 800-208](https://csrc.nist.gov/publications/detail/sp/800-208/final)
- [CWE Top 25](https://cwe.mitre.org/top25/)

### Support Channels
- **Issues**: [GitHub Issues](https://github.com/VISENDI56/iLuminara-Core/issues)
- **Security**: Report vulnerabilities via GitHub Security Advisories
- **Documentation**: [docs/](../docs/) directory

---

## 📝 Maintenance

### Regular Tasks

#### Weekly
- Review security findings in GitHub Security tab
- Address any new vulnerabilities
- Monitor scan performance metrics

#### Monthly
- Update detection patterns for new threat intel
- Review and tune false positive rates
- Verify 90-day audit retention

#### Quarterly
- Compliance audit against NIST frameworks
- Performance benchmarking
- Update documentation

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0 | 2024-12-21 | Initial production release |
| | | - Dual-mode operation |
| | | - 6 secret patterns |
| | | - 5 SAST patterns |
| | | - SARIF output |
| | | - Jetson Orin optimization |

---

## 🔐 Security Considerations

### Baseline Integrity
- Store `integrity_ledger.json` in version control
- Treat baseline updates as critical security events
- Require code review for baseline modifications
- Sign commits that update the baseline (recommended)

### Secret Management
- **Never commit real secrets** to any repository
- Use environment variables or secret management systems
- Rotate credentials if accidentally committed
- GitHub will also scan for leaked secrets independently

### SARIF Report Handling
- SARIF reports may contain code snippets
- Ensure `.gitignore` excludes `*.sarif` files
- Review reports before sharing externally
- Store reports securely with appropriate access controls

---

**🚀 Sentinel v3.0 - Sovereign DevSecOps for Critical Infrastructure**

*Engineered for iLuminara Biosecurity | NIST-Compliant | Edge-Optimized*
