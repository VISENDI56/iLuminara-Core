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
    source "${SCRIPT_DIR}/modules/e2i_056_enforcer.sh"
    run_e2i_prune_target
else
    log_sovereign "OCCAM KERNEL: Dry-run mode - analysis only"
fi
log_sovereign "Sovereign OS $(python3 version.py | tail -1): System Nominal."
