#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/isf_config.sh"
source "${SCRIPT_DIR}/modules/valley_standards.sh"
verify_integrity
run_valley_standards_sync
# Z3-Gate Pre-Check
if [ "${1:-}" != "--dry-run" ]; then
    source "${SCRIPT_DIR}/modules/occam_kernel.sh"
    run_occam_pruning
else
    log_sovereign "OCCAM KERNEL: Dry-run mode - analysis only"
fi
log_sovereign "Sovereign OS Rev 171: System Nominal."
