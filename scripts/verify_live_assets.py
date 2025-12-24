#!/usr/bin/env python3
"""
Live Assets Verification Script
═════════════════════════════════════════════════════════════════════════════

Performs smoke testing on live URLs and confirms they load correctly.
This ensures zero 403/404 errors across documentation and web assets.

Philosophy: "Trust, but verify. Every endpoint. Every time."
"""

import sys
import requests
from typing import List, Dict, Tuple
from datetime import datetime
import json

# Configuration
TIMEOUT = 10  # seconds
USER_AGENT = "iLuminara-Asset-Verifier/1.0"

# The Sovereign Asset List
ASSETS = [
    # Mintlify Documentation
    {
        "url": "https://visendi56.mintlify.app/",
        "name": "Mintlify Homepage",
        "type": "documentation",
        "required": True
    },
    {
        "url": "https://visendi56.mintlify.app/docs/introduction",
        "name": "Introduction",
        "type": "documentation",
        "required": True
    },
    {
        "url": "https://visendi56.mintlify.app/docs/architecture",
        "name": "Architecture",
        "type": "documentation",
        "required": True
    },
    {
        "url": "https://visendi56.mintlify.app/docs/quickstart",
        "name": "Quickstart",
        "type": "documentation",
        "required": True
    },
    {
        "url": "https://visendi56.mintlify.app/docs/nuclear-ip/crypto-shredder",
        "name": "Crypto Shredder (IP-02)",
        "type": "documentation",
        "required": True
    },
    {
        "url": "https://visendi56.mintlify.app/docs/nuclear-ip/somatic-auth",
        "name": "Somatic Auth (IP-03)",
        "type": "documentation",
        "required": True
    },
    {
        "url": "https://visendi56.mintlify.app/docs/nuclear-ip/serenity-flow",
        "name": "Serenity Flow (IP-04)",
        "type": "documentation",
        "required": True
    },
    {
        "url": "https://visendi56.mintlify.app/docs/nuclear-ip/golden-thread",
        "name": "Golden Thread (IP-05)",
        "type": "documentation",
        "required": True
    },
    {
        "url": "https://visendi56.mintlify.app/docs/nuclear-ip/viral-bridge",
        "name": "Viral Bridge (IP-06)",
        "type": "documentation",
        "required": True
    },
    {
        "url": "https://visendi56.mintlify.app/docs/governance/rco-engine",
        "name": "RCO Engine",
        "type": "documentation",
        "required": True
    },
    {
        "url": "https://visendi56.mintlify.app/docs/governance/45-laws",
        "name": "45-Law Nexus",
        "type": "documentation",
        "required": True
    },
    {
        "url": "https://visendi56.mintlify.app/api-reference/introduction",
        "name": "API Introduction",
        "type": "documentation",
        "required": True
    },
    {
        "url": "https://visendi56.mintlify.app/api-reference/endpoints",
        "name": "API Endpoints",
        "type": "documentation",
        "required": True
    },
    # GitHub Repository
    {
        "url": "https://github.com/VISENDI56/iLuminara-Core",
        "name": "GitHub Repository",
        "type": "repository",
        "required": True
    },
]


class AssetVerifier:
    """Verifies live assets and generates a detailed report."""
    
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
    
    def verify_url(self, asset: Dict) -> Tuple[bool, Dict]:
        """
        Verify a single URL.
        
        Args:
            asset: Asset dictionary with url, name, type, required
            
        Returns:
            Tuple of (success, result_dict)
        """
        url = asset["url"]
        name = asset["name"]
        
        result = {
            "name": name,
            "url": url,
            "type": asset["type"],
            "required": asset["required"],
            "status_code": None,
            "success": False,
            "error": None,
            "response_time_ms": None
        }
        
        try:
            headers = {"User-Agent": USER_AGENT}
            response = requests.get(url, headers=headers, timeout=TIMEOUT, allow_redirects=True)
            
            result["status_code"] = response.status_code
            result["response_time_ms"] = int(response.elapsed.total_seconds() * 1000)
            
            # Consider 200 and 3xx redirects as success
            if 200 <= response.status_code < 400:
                result["success"] = True
            else:
                result["error"] = f"HTTP {response.status_code}"
            
        except requests.exceptions.Timeout:
            result["error"] = "Timeout (>10s)"
        except requests.exceptions.ConnectionError:
            result["error"] = "Connection Failed"
        except requests.exceptions.TooManyRedirects:
            result["error"] = "Too Many Redirects"
        except requests.exceptions.RequestException as e:
            result["error"] = f"Request Error: {str(e)}"
        except Exception as e:
            result["error"] = f"Unexpected Error: {str(e)}"
        
        return result["success"], result
    
    def verify_all(self) -> Dict:
        """
        Verify all assets and generate comprehensive report.
        
        Returns:
            Dictionary with verification results
        """
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 25 + "ASSET VERIFICATION PROTOCOL" + " " * 25 + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        
        total = len(ASSETS)
        passed = 0
        failed = 0
        
        for i, asset in enumerate(ASSETS, 1):
            print(f"[{i}/{total}] Verifying: {asset['name']}")
            print(f"         URL: {asset['url']}")
            
            success, result = self.verify_url(asset)
            self.results.append(result)
            
            if success:
                print(f"         ✅ Status: {result['status_code']} ({result['response_time_ms']}ms)")
                passed += 1
            else:
                status_indicator = "🔴" if asset["required"] else "⚠️"
                print(f"         {status_indicator} FAILED: {result['error']}")
                failed += 1
            
            print()
        
        # Generate summary
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        report = {
            "timestamp": end_time.isoformat(),
            "duration_seconds": duration,
            "total_assets": total,
            "passed": passed,
            "failed": failed,
            "success_rate": (passed / total * 100) if total > 0 else 0,
            "results": self.results
        }
        
        # Print summary
        print("═" * 80)
        print("  VERIFICATION SUMMARY")
        print("═" * 80)
        print()
        print(f"Total Assets Checked: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} {'🔴' if failed > 0 else '✅'}")
        print(f"Success Rate: {report['success_rate']:.1f}%")
        print(f"Duration: {duration:.2f}s")
        print()
        
        if failed > 0:
            print("Failed Assets:")
            for result in self.results:
                if not result["success"]:
                    required_indicator = " (REQUIRED)" if result["required"] else ""
                    print(f"  🔴 {result['name']}{required_indicator}")
                    print(f"     URL: {result['url']}")
                    print(f"     Error: {result['error']}")
            print()
        
        # Determine overall status
        required_failed = sum(1 for r in self.results if not r["success"] and r["required"])
        
        if required_failed == 0:
            print("╔" + "═" * 78 + "╗")
            print("║" + " " * 24 + "✅ ALL REQUIRED ASSETS VERIFIED" + " " * 23 + "║")
            print("╚" + "═" * 78 + "╝")
            print()
            print("Status: READY FOR MARKETPLACE DEPLOYMENT")
        else:
            print("╔" + "═" * 78 + "╗")
            print("║" + " " * 24 + "🔴 REQUIRED ASSETS FAILED" + " " * 29 + "║")
            print("╚" + "═" * 78 + "╝")
            print()
            print("Status: FIX REQUIRED BEFORE DEPLOYMENT")
        
        print("═" * 80)
        
        return report


def main():
    """Execute asset verification."""
    verifier = AssetVerifier()
    report = verifier.verify_all()
    
    # Save report to file
    report_path = "asset_verification_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nDetailed report saved to: {report_path}")
    
    # Return exit code based on required assets
    required_failed = sum(1 for r in report["results"] if not r["success"] and r["required"])
    return 0 if required_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
