"""
THE SENTINEL v3.0: Sovereign DevSecOps Engine
Compliance: NIST SP 800-208 | Target: Jetson Orin Edge
Capabilities: Secret Scanning, Integrity Verification, SAST, SARIF Output
"""
import os
import re
import hashlib
import sys
import json
import argparse
from datetime import datetime

# CONFIGURATION
LEDGER_FILE = "enterprise/integrity_ledger.json"
MAX_FILE_SIZE_MB = 10  # Skip files larger than 10MB (Model Weights)
SKIP_DIRS = {".git", "venv", "__pycache__", "logs", "node_modules", ".venv"}
SKIP_EXTS = {".pyc", ".png", ".jpg", ".tflite", ".bin", ".pt", ".pth", ".onnx"}

class Sentinel:
    def __init__(self, mode="SCAN"):
        self.mode = mode
        self.root_dir = "."
        self.vulnerabilities = []
        self.ledger = self._load_ledger()
        self.new_ledger = {}
        self.files_scanned = 0

    def _load_ledger(self):
        """Load existing integrity baseline"""
        if os.path.exists(LEDGER_FILE):
            try:
                with open(LEDGER_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️  Warning: Corrupted ledger file at {LEDGER_FILE}")
                return {}
        return {}

    def _calculate_hash(self, filepath):
        """Streaming SHA-256 for memory efficiency on Edge"""
        sha256 = hashlib.sha256()
        try:
            # Check file size first
            file_size = os.path.getsize(filepath)
            if file_size > (MAX_FILE_SIZE_MB * 1024 * 1024):
                return "SKIPPED_LARGE_FILE"
            
            if file_size == 0:
                return "EMPTY_FILE"
                
            # Use 64KB chunks for better I/O performance
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except (OSError, IOError) as e:
            print(f"   ⚠️  Cannot read {filepath}: {e}")
            return None

    def scan_sast_patterns(self, content, filepath):
        """Static Application Security Testing (SAST)"""
        # Note: Patterns are designed to catch common credential formats
        # Some false positives may occur for pattern definitions in code/docs
        patterns = [
            (r"eval\(", "CWE-95", "Code Injection Risk (eval)"),
            (r"exec\(", "CWE-95", "Code Injection Risk (exec)"),
            (r"pickle\.loads", "CWE-502", "Insecure Deserialization"),
            (r"os\.system\(", "CWE-78", "OS Command Injection"),
            (r"subprocess\.call\(.*shell=True", "CWE-78", "Shell Injection Risk"),
            (r"AIza[0-9A-Za-z-_]{35}", "SEC-001", "Secret: Google API Key"),
            (r"sk-[a-zA-Z0-9]{32,}", "SEC-002", "Secret: OpenAI API Key"),
            (r"(?i)AKIA[0-9A-Z]{16}", "SEC-003", "Secret: AWS Access Key"),
            (r"-----BEGIN PRIVATE KEY-----", "SEC-004", "Secret: Private Key (PEM)"),
            (r"ghp_[a-zA-Z0-9]{36}", "SEC-005", "Secret: GitHub Token"),
            (r"postgres://[^:]+:[^@]+@", "SEC-006", "Secret: Database Connection String")
        ]
        
        lines = content.split('\n')
        for line_num, line in enumerate(lines, start=1):
            for pattern, rule_id, description in patterns:
                if re.search(pattern, line):
                    self.add_issue(
                        rule_id, 
                        f"Dangerous pattern: {description}", 
                        filepath,
                        "error" if "Secret" in description else "warning",
                        line_num,
                        line.strip()[:100]  # Truncate long lines
                    )

    def run(self):
        """Main execution loop"""
        print(f"╔════════ SENTINEL v3.0 ({self.mode}) ════════╗")
        print(f"   Root: {os.path.abspath(self.root_dir)}")
        print(f"   Mode: {self.mode}")
        print("═" * 48)
        
        for root, dirs, files in os.walk(self.root_dir):
            # Prune directories in-place
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            
            for file in files:
                # Skip by extension
                if any(file.endswith(ext) for ext in SKIP_EXTS):
                    continue
                
                # Skip hidden files
                if file.startswith('.'):
                    continue
                
                path = os.path.join(root, file)
                relative_path = os.path.relpath(path, self.root_dir)
                
                # Calculate hash
                current_hash = self._calculate_hash(path)
                
                if current_hash in ["SKIPPED_LARGE_FILE", None]:
                    continue
                
                self.files_scanned += 1
                
                # MODE 1: BASELINE GENERATION
                if self.mode == "BASELINE":
                    self.new_ledger[relative_path] = current_hash
                    if self.files_scanned % 10 == 0:
                        print(f"   [+] Hashed {self.files_scanned} files...")

                # MODE 2: SECURITY SCAN
                elif self.mode == "SCAN":
                    # Integrity Check
                    if relative_path in self.ledger:
                        if self.ledger[relative_path] != current_hash:
                            self.add_issue(
                                "INT-001", 
                                "Integrity Violation: File Modified Since Baseline",
                                relative_path,
                                "critical"
                            )
                    
                    # SAST & Secret Scanning (only on code files)
                    if file.endswith((".py", ".sh", ".json", ".md", ".yaml", ".yml", ".env", 
                                     ".js", ".ts", ".php", ".rb", ".go", ".java")):
                        try:
                            with open(path, "r", errors="replace") as f:
                                content = f.read()
                                self.scan_sast_patterns(content, relative_path)
                        except Exception as e:
                            print(f"   ⚠️  Cannot scan {relative_path}: {e}")

        # FINALIZE
        if self.mode == "BASELINE":
            os.makedirs(os.path.dirname(LEDGER_FILE), exist_ok=True)
            with open(LEDGER_FILE, 'w') as f:
                json.dump(self.new_ledger, f, indent=2, sort_keys=True)
            print(f"\n✅ GOLDEN STATE LOCKED: {len(self.new_ledger)} files hashed.")
            print(f"   Ledger saved to: {LEDGER_FILE}")
            
        elif self.mode == "SCAN":
            self.save_sarif()
            print(f"\n📊 SCAN COMPLETE: {self.files_scanned} files analyzed")
            
            if self.vulnerabilities:
                critical = sum(1 for v in self.vulnerabilities if v.get('level') == 'critical')
                errors = sum(1 for v in self.vulnerabilities if v.get('level') == 'error')
                warnings = sum(1 for v in self.vulnerabilities if v.get('level') == 'warning')
                
                print(f"   🔴 Critical: {critical}")
                print(f"   🟠 Errors:   {errors}")
                print(f"   🟡 Warnings: {warnings}")
                print(f"\n❌ SECURITY GATE FAILED: {len(self.vulnerabilities)} issues found.")
                sys.exit(1)
            else:
                print("✅ SYSTEM SECURE. NO THREATS DETECTED.")
                sys.exit(0)

    def add_issue(self, rule_id, message, filepath, level, line_num=1, snippet=""):
        """Add vulnerability to report"""
        print(f"   [{level.upper()}] {rule_id}: {message}")
        print(f"           File: {filepath}:{line_num}")
        
        self.vulnerabilities.append({
            "ruleId": rule_id,
            "message": {"text": message},
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {"uri": filepath},
                    "region": {
                        "startLine": line_num,
                        "snippet": {"text": snippet} if snippet else {}
                    }
                }
            }],
            "level": level
        })

    def save_sarif(self):
        """Generate GitHub-Compatible SARIF Report"""
        sarif_report = {
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
                "results": self.vulnerabilities
            }]
        }
        
        with open("sentinel_report.sarif", "w") as f:
            json.dump(sarif_report, f, indent=2)
        print(f"   📄 SARIF report saved: sentinel_report.sarif")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sentinel v3.0: Sovereign DevSecOps Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Generate baseline:    python sentinel.py --mode BASELINE
  Run security scan:    python sentinel.py --mode SCAN
        """
    )
    parser.add_argument(
        "--mode", 
        choices=["SCAN", "BASELINE"], 
        default="SCAN",
        help="Operation mode (default: SCAN)"
    )
    
    args = parser.parse_args()
    
    try:
        Sentinel(mode=args.mode).run()
    except KeyboardInterrupt:
        print("\n⚠️  Scan interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
