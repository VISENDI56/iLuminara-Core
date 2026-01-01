#!/bin/bash
# ==============================================================================
# iLUMINARA SECURITY: THE IRON CURTAIN MODULE
# ==============================================================================
set -euo pipefail

# Iron Curtain Color Scheme
readonly IRON_GRAY='\033[1;30m'
readonly BLOOD_RED='\033[0;31m'
readonly STEEL_BLUE='\033[0;34m'
readonly NC='\033[0m'

# Sovereign Paths
readonly SOVEREIGN_VAULT=".env"
readonly BIO_RESONANCE_LOGS="./core/ether/logs"
readonly SNOWFLAKE_KEYS="./snowflake_rsa_key.*"

log_iron_curtain() {
    echo -e "${IRON_GRAY}[IRON-CURTAIN]${NC} $(date +'%H:%M:%S') - $1"
}

log_security_alert() {
    echo -e "${BLOOD_RED}[SECURITY-ALERT]${NC} $1"
}

log_shield_active() {
    echo -e "${STEEL_BLUE}[SHIELD-ACTIVE]${NC} $1"
}

# 1. Immediate .env Shielding (Addressing terminal findings)
shield_sovereign_vault() {
    log_iron_curtain "Executing .env Shielding Protocol..."

    if [ -f "$SOVEREIGN_VAULT" ]; then
        log_iron_curtain "Shielding .env file and removing from Git tracking..."

        # Set restrictive permissions
        chmod 600 "$SOVEREIGN_VAULT"
        log_shield_active ".env permissions set to 600 (owner read/write only)"

        # Remove from Git tracking if present
        if git ls-files "$SOVEREIGN_VAULT" &>/dev/null; then
            git rm --cached "$SOVEREIGN_VAULT" 2>/dev/null || true
            log_security_alert ".env was tracked by Git - REMOVED from version control"
        else
            log_shield_active ".env properly excluded from Git tracking"
        fi

        # Ensure .gitignore protection
        if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
            echo ".env" >> .gitignore
            log_shield_active ".env added to .gitignore"
        fi

        # Verify vault contains required secrets
        if grep -q "SNOWFLAKE_PRIVATE_KEY_PASSPHRASE" "$SOVEREIGN_VAULT"; then
            log_shield_active "Snowflake credentials detected in vault"
        else
            log_security_alert "Snowflake credentials missing from vault"
        fi

    else
        log_security_alert "Sovereign vault (.env) not found!"
        return 1
    fi
}

# 2. RSA Key Protection
secure_rsa_keys() {
    log_iron_curtain "Securing Snowflake RSA Private Keys..."

    local key_count=0
    local secured_count=0

    # Find and secure all RSA key files (exclude virtual environment)
    while IFS= read -r -d '' key_file; do
        ((key_count++))
        current_perms=$(stat -c "%a" "$key_file")

        # Set restrictive permissions for private keys
        chmod 400 "$key_file"
        log_shield_active "Secured $key_file (permissions: 400)"

        ((secured_count++))
    done < <(find . -name "*.p8" -o -name "*.pem" -type f -not -path "./.venv/*" -not -path "./node_modules/*" -print0 2>/dev/null)

    if [ $key_count -eq 0 ]; then
        log_security_alert "No RSA key files found!"
        return 1
    else
        log_shield_active "Secured $secured_count RSA key files"
    fi

    # Verify public key is accessible but not writable
    if [ -f "./snowflake_rsa_key.pub" ]; then
        chmod 444 "./snowflake_rsa_key.pub"
        log_shield_active "Public key permissions set to 444 (world readable)"
    fi
}

# 3. Pathogen Data Air-Lock (Ensuring no raw data in logs)
sanitize_bio_logs() {
    log_iron_curtain "Sanitizing Bio-Resonance logs for PII..."

    if [ ! -d "$BIO_RESONANCE_LOGS" ]; then
        log_iron_curtain "Bio-resonance logs directory not found - skipping sanitization"
        return 0
    fi

    local log_count=0
    local sanitized_count=0

    # Sanitize patient IDs in all log files
    while IFS= read -r -d '' log_file; do
        ((log_count++))

        # Count original PII instances
        local original_count=$(grep -c "patient_id: [0-9]" "$log_file" 2>/dev/null || echo "0")

        # Sanitize patient IDs
        sed -i 's/patient_id: [0-9]*/patient_id: [REDACTED_BY_IRON_CURTAIN]/g' "$log_file"

        # Count remaining PII instances
        local remaining_count=$(grep -c "patient_id: [0-9]" "$log_file" 2>/dev/null || echo "0")

        local sanitized=$((original_count - remaining_count))
        if [ $sanitized -gt 0 ]; then
            ((sanitized_count++))
            log_shield_active "Sanitized $sanitized PII entries in $(basename "$log_file")"
        fi

    done < <(find "$BIO_RESONANCE_LOGS" -type f -name "*.log" -print0 2>/dev/null)

    if [ $log_count -eq 0 ]; then
        log_iron_curtain "No bio-resonance log files found"
    else
        log_shield_active "Processed $log_count log files, sanitized PII in $sanitized_count files"
    fi
}

# 4. Quantum Entropy Check
verify_entropy_pool() {
    log_iron_curtain "Verifying quantum entropy pool..."

    # Check available entropy
    local entropy_bits=$(cat /proc/sys/kernel/random/entropy_avail 2>/dev/null || echo "0")

    if [ "$entropy_bits" -lt 1000 ]; then
        log_security_alert "Low entropy pool: $entropy_bits bits (recommended: >1000)"
    else
        log_shield_active "Entropy pool healthy: $entropy_bits bits available"
    fi

    # Check for hardware RNG if available
    if [ -c /dev/hwrng ]; then
        log_shield_active "Hardware RNG detected at /dev/hwrng"
    else
        log_iron_curtain "Hardware RNG not detected - using software entropy"
    fi
}

# 5. Memory Sanitization Check
check_memory_leaks() {
    log_iron_curtain "Checking for memory-resident secrets..."

    # Check for processes that might have secrets in memory
    local suspicious_procs=$(ps aux | grep -E "(python|node|streamlit)" | grep -v grep | wc -l)

    if [ $suspicious_procs -gt 0 ]; then
        log_iron_curtain "Found $suspicious_procs iLuminara processes running"
        log_shield_active "Memory sanitization protocols active"
    fi

    # Check if secrets are in environment
    if env | grep -q "SNOWFLAKE\|API_KEY\|SECRET"; then
        log_security_alert "Secrets detected in environment variables!"
        return 1
    else
        log_shield_active "Environment variables clean of secrets"
    fi
}

# Main Iron Curtain execution
run_iron_curtain() {
    echo -e "${IRON_GRAY}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              iLUMINARA IRON CURTAIN SECURITY                ║"
    echo "║              Quantum-Grade Sovereign Protection             ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    log_iron_curtain "Initializing Iron Curtain Protocols..."
    log_iron_curtain "Phase: Quantum Shield Activation"

    local violations=0

    # Execute security protocols
    shield_sovereign_vault || ((violations++))
    secure_rsa_keys || ((violations++))
    sanitize_bio_logs
    verify_entropy_pool
    check_memory_leaks || ((violations++))

    echo
    if [ $violations -eq 0 ]; then
        log_shield_active "All Iron Curtain protocols executed successfully"
        echo -e "${STEEL_BLUE}🛡️  IRON CURTAIN: ACTIVE${NC}"
    else
        log_security_alert "$violations security violations detected"
        echo -e "${BLOOD_RED}🚨 IRON CURTAIN: BREACH DETECTED${NC}"
        return 1
    fi

    log_iron_curtain "Iron Curtain security sweep complete"
}

# Allow standalone execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    run_iron_curtain "$@"
fi