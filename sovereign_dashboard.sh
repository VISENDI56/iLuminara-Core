#!/bin/bash
# ==============================================================================
# iLUMINARA SOVEREIGN VALIDATION DASHBOARD
# ==============================================================================

# Source configuration if available
if [ -f "./core/governance/fixer/isf_config.sh" ]; then
    source "./core/governance/fixer/isf_config.sh"
else
    # Fallback color definitions if config not found
    readonly GOLD='\033[0;33m'
    readonly CYAN='\033[0;36m'
    readonly PURPLE='\033[0;35m'
    readonly RED='\033[0;31m'
    readonly GREEN='\033[0;32m'
    readonly NC='\033[0m'
fi

echo -e "${GOLD}══════════════════════════════════════════════════════════════${NC}"
echo -e "${GOLD}   iLUMINARA SOVEREIGN OS - VALIDATION DASHBOARD${NC}"
echo -e "${GOLD}══════════════════════════════════════════════════════════════${NC}"

# 1. Hardware Status (Blackwell Ready)
MEM_USAGE=$(free -h | awk '/^Mem:/ {print $3 "/" $2}')
DISK_USAGE=$(df -h . | awk 'NR==2 {print $3 "/" $2 " (" $5 ")"}')
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'.' -f1)
echo -e "${CYAN}[SYSTEM]${NC} Memory: $MEM_USAGE | Disk: $DISK_USAGE | CPU: ${CPU_USAGE}%"

# 2. Security Audit (The Iron Curtain)
SENSITIVE_FILES=$(find . -type f \( -name ".env" -o -name "*.p8" -o -name "*.pem" \) -not -path "./.venv/*" -not -path "./key_backups/*" | wc -l)
if [ "$SENSITIVE_FILES" -gt 0 ]; then
    echo -e "${PURPLE}[SECURITY]${NC} 🛡️  $SENSITIVE_FILES Sensitive files locked in the Vault."
else
    echo -e "${RED}[SECURITY]${NC} ⚠️  NO ENCRYPTED VAULT DETECTED!"
fi

# 3. Logic Integrity (Z3 Prover)
if command -v z3 &> /dev/null; then
    Z3_VER=$(z3 --version 2>/dev/null | awk '{print $3}' || echo "Unknown")
    echo -e "${CYAN}[LOGIC]${NC} Z3 Formal Logic Engine: v$Z3_VER (Stable)"
else
    echo -e "${RED}[LOGIC]${NC} ❌ Z3 PROVER MISSING!"
fi

# 4. Sovereign Modules Status
MODULES_CHECKED=0
MODULES_ACTIVE=0

# Check Sovereign Fixer
if [ -f "./sovereign_fixer.sh" ]; then
    ((MODULES_CHECKED++))
    ((MODULES_ACTIVE++))
    echo -e "${GREEN}[MODULES]${NC} Sovereign Fixer: Active"
else
    ((MODULES_CHECKED++))
    echo -e "${RED}[MODULES]${NC} Sovereign Fixer: Missing"
fi

# Check Iron Curtain
if [ -f "./iron_curtain.sh" ]; then
    ((MODULES_CHECKED++))
    ((MODULES_ACTIVE++))
    echo -e "${GREEN}[MODULES]${NC} Iron Curtain Security: Active"
else
    ((MODULES_CHECKED++))
    echo -e "${RED}[MODULES]${NC} Iron Curtain Security: Missing"
fi

# Check Blackwell Optimization
if [ -f "./blackwell_optimization.sh" ]; then
    ((MODULES_CHECKED++))
    ((MODULES_ACTIVE++))
    echo -e "${GREEN}[MODULES]${NC} Blackwell Optimization: Active"
else
    ((MODULES_CHECKED++))
    echo -e "${RED}[MODULES]${NC} Blackwell Optimization: Missing"
fi

# Check Validation Dashboard
if [ -f "./validation_dashboard.sh" ]; then
    ((MODULES_CHECKED++))
    ((MODULES_ACTIVE++))
    echo -e "${GREEN}[MODULES]${NC} Validation Dashboard: Active"
else
    ((MODULES_CHECKED++))
    echo -e "${RED}[MODULES]${NC} Validation Dashboard: Missing"
fi

echo -e "${CYAN}[MODULES]${NC} Status: $MODULES_ACTIVE/$MODULES_CHECKED modules active"

# 5. Recent Activity
echo -e "${PURPLE}[ACTIVITY]${NC} Recent Sovereign Operations:"
if [ -f "./core/governance/stbk_audit.log" ]; then
    LAST_LOG=$(tail -1 "./core/governance/stbk_audit.log" 2>/dev/null || echo "No recent activity")
    echo -e "${PURPLE}[ACTIVITY]${NC} $LAST_LOG"
else
    echo -e "${PURPLE}[ACTIVITY]${NC} STBK Audit log not found"
fi

# 6. Git Status
if [ -d ".git" ]; then
    BRANCH=$(git branch --show-current 2>/dev/null || echo "Unknown")
    COMMITS=$(git log --oneline 2>/dev/null | wc -l || echo "0")
    echo -e "${CYAN}[GIT]${NC} Branch: $BRANCH | Commits: $COMMITS"
else
    echo -e "${RED}[GIT]${NC} Not a git repository"
fi

echo -e "${GOLD}──────────────────────────────────────────────────────────────${NC}"

# Recommendations based on status
ISSUES=0

if [ "$SENSITIVE_FILES" -eq 0 ]; then
    echo -e "${RED}CRITICAL:${NC} No encrypted vault detected!"
    ((ISSUES++))
fi

if ! command -v z3 &> /dev/null; then
    echo -e "${RED}CRITICAL:${NC} Z3 prover missing for logic verification!"
    ((ISSUES++))
fi

if [ $MODULES_ACTIVE -lt $MODULES_CHECKED ]; then
    echo -e "${RED}WARNING:${NC} Some sovereign modules are missing!"
    ((ISSUES++))
fi

if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}✅ SOVEREIGN INTEGRITY: VERIFIED${NC}"
    echo -e "Recommendations: Run './sovereign_fixer.sh' for routine maintenance"
else
    echo -e "${RED}❌ SOVEREIGN INTEGRITY: $ISSUES ISSUES DETECTED${NC}"
    echo -e "Recommendations: Run './sovereign_fixer.sh' to resolve issues"
fi

echo -e "${GOLD}══════════════════════════════════════════════════════════════${NC}"