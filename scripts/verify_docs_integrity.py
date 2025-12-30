# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------

#!/usr/bin/env python3
"""
Documentation Integrity Checker
═════════════════════════════════════════════════════════════════════════════

Verifies that all documentation files referenced in mint.json actually exist
and that the navigation structure is complete.

This is a local alternative to `mintlify broken-links` for offline verification.

Philosophy: "Documentation is the interface to your genius. Verify every link."
"""

import sys
import json
import os
from pathlib import Path
from typing import List, Dict, Tuple, Set

# Repository root
REPO_ROOT = Path(__file__).parent.parent

# Supported documentation file extensions
DOC_EXTENSIONS = [".mdx", ".md"]


class DocumentationVerifier:
    """Verifies documentation structure integrity."""
    
    def __init__(self):
        self.mint_json_path = REPO_ROOT / "mint.json"
        self.errors = []
        self.warnings = []
        self.checked_files = set()
    
    def verify(self) -> bool:
        """
        Run complete verification.
        
        Returns:
            True if all checks pass, False otherwise
        """
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 22 + "DOCUMENTATION INTEGRITY CHECKER" + " " * 25 + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        
        # Step 1: Verify mint.json exists and is valid JSON
        if not self.verify_mint_json():
            return False
        
        # Step 2: Load mint.json
        mint_config = self.load_mint_json()
        if not mint_config:
            return False
        
        # Step 3: Verify navigation structure
        self.verify_navigation(mint_config)
        
        # Step 4: Check for orphaned MDX files
        self.check_orphaned_files()
        
        # Step 5: Print summary
        self.print_summary()
        
        return len(self.errors) == 0
    
    def verify_mint_json(self) -> bool:
        """Verify mint.json exists."""
        if not self.mint_json_path.exists():
            self.errors.append(f"mint.json not found at {self.mint_json_path}")
            return False
        
        print(f"✅ Found mint.json at {self.mint_json_path}")
        return True
    
    def load_mint_json(self) -> Dict:
        """Load and parse mint.json."""
        try:
            with open(self.mint_json_path, 'r') as f:
                config = json.load(f)
            print("✅ mint.json is valid JSON")
            return config
        except json.JSONDecodeError as e:
            self.errors.append(f"mint.json is invalid JSON: {e}")
            return None
        except Exception as e:
            self.errors.append(f"Failed to read mint.json: {e}")
            return None
    
    def verify_navigation(self, config: Dict):
        """Verify all pages in navigation exist."""
        print("\n📋 Verifying navigation structure...")
        print()
        
        navigation = config.get("navigation", [])
        
        if not navigation:
            self.warnings.append("No navigation defined in mint.json")
            return
        
        for group in navigation:
            group_name = group.get("group", "Unknown")
            pages = group.get("pages", [])
            
            print(f"Group: {group_name}")
            
            for page_path in pages:
                self.verify_page(page_path)
    
    def verify_page(self, page_path: str):
        """Verify a single page exists."""
        # Try different extensions
        possible_paths = [
            REPO_ROOT / f"{page_path}{ext}" for ext in DOC_EXTENSIONS
        ] + [REPO_ROOT / page_path]
        
        found = False
        actual_path = None
        
        for path in possible_paths:
            if path.exists():
                found = True
                actual_path = path
                self.checked_files.add(str(path.relative_to(REPO_ROOT)))
                break
        
        if found:
            print(f"  ✅ {page_path}")
        else:
            print(f"  🔴 {page_path} (NOT FOUND)")
            self.errors.append(f"Missing file for navigation entry: {page_path}")
            
            # Suggest possible fixes
            page_name = Path(page_path).name
            similar_files = self.find_similar_files(page_name)
            if similar_files:
                self.warnings.append(
                    f"  → Did you mean one of these? {', '.join(similar_files[:3])}"
                )
    
    def find_similar_files(self, name: str) -> List[str]:
        """Find files with similar names."""
        similar = []
        docs_dir = REPO_ROOT / "docs"
        api_ref_dir = REPO_ROOT / "api-reference"
        
        for directory in [docs_dir, api_ref_dir]:
            if not directory.exists():
                continue
            
            for ext in DOC_EXTENSIONS:
                for doc_file in directory.rglob(f"*{ext}"):
                    if name in doc_file.stem or doc_file.stem in name:
                        rel_path = doc_file.relative_to(REPO_ROOT)
                        similar.append(str(rel_path))
        
        return similar
    
    def check_orphaned_files(self):
        """Check for documentation files not referenced in navigation."""
        print("\n📂 Checking for orphaned files...")
        print()
        
        all_doc_files = set()
        
        # Find all documentation files
        for directory in [REPO_ROOT / "docs", REPO_ROOT / "api-reference"]:
            if not directory.exists():
                continue
            
            for ext in DOC_EXTENSIONS:
                for doc_file in directory.rglob(f"*{ext}"):
                    rel_path = str(doc_file.relative_to(REPO_ROOT))
                    all_doc_files.add(rel_path)
        
        # Find orphaned files
        orphaned = all_doc_files - self.checked_files
        
        if orphaned:
            print("⚠️  Found files not in navigation:")
            for file_path in sorted(orphaned):
                print(f"  - {file_path}")
                self.warnings.append(f"Orphaned file not in navigation: {file_path}")
        else:
            print("✅ No orphaned files found")
    
    def print_summary(self):
        """Print verification summary."""
        print("\n" + "═" * 80)
        print("  VERIFICATION SUMMARY")
        print("═" * 80)
        print()
        
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        print()
        
        if self.errors:
            print("🔴 ERRORS:")
            for error in self.errors:
                print(f"  - {error}")
            print()
        
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
            print()
        
        if not self.errors:
            print("╔" + "═" * 78 + "╗")
            print("║" + " " * 24 + "✅ DOCUMENTATION VERIFIED" + " " * 29 + "║")
            print("╚" + "═" * 78 + "╝")
            print()
            print("Status: DOCUMENTATION STRUCTURE IS VALID")
        else:
            print("╔" + "═" * 78 + "╗")
            print("║" + " " * 26 + "🔴 ERRORS FOUND" + " " * 37 + "║")
            print("╚" + "═" * 78 + "╝")
            print()
            print("Status: FIX ERRORS BEFORE DEPLOYMENT")
        
        print("═" * 80)


def main():
    """Execute documentation verification."""
    verifier = DocumentationVerifier()
    success = verifier.verify()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
