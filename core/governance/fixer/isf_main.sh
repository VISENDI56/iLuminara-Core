#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/isf_config.sh"
source "${SCRIPT_DIR}/modules/valley_standards.sh"
verify_integrity
run_valley_standards_sync
log_sovereign "Sovereign OS Rev 168: System Nominal."
