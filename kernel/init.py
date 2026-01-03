#!/usr/bin/env python3
"""
Initialize the Governance Kernel with specified frameworks.
"""
import sys
import argparse
from legal_vector import LegalVectorLedger

def main():
    parser = argparse.ArgumentParser(description='Initialize iLuminara Governance Kernel')
    parser.add_argument('--framework', action='append', help='Legal framework to enable')
    parser.add_argument('--region', default='FIELD_HOSPITAL', help='Deployment region')
    parser.add_argument('--jurisdiction', default='GLOBAL', help='Legal jurisdiction')
    
    args = parser.parse_args()
    
    ledger = LegalVectorLedger(jurisdiction=args.jurisdiction)
    
    print(f"✅ Governance Kernel Initialized")
    print(f"   Region: {args.region}")
    print(f"   Jurisdiction: {args.jurisdiction}")
    print(f"   Frameworks: {args.framework or ['Default']}")
    print(f"   Total frameworks: {len(ledger.frameworks)}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
