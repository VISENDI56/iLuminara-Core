#!/bin/bash
# Validation Dashboard for GitHub Codespace

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║    ENTERPRISE VALIDATION DASHBOARD       ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""

# Check system health
echo "📊 System Health:"
echo "----------------"
echo "  Memory: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
echo "  Disk: $(df -h . | awk 'NR==2 {print $3 "/" $2 " (" $5 ")"}')"
echo "  CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')%"
echo ""

# Git status
echo "🌿 Git Status:"
echo "------------"
if [ -d ".git" ]; then
    BRANCH=$(git branch --show-current)
        COMMITS=$(git log --oneline | wc -l)
            echo "  Branch: $BRANCH"
                echo "  Commits: $COMMITS"
                    echo "  Last commit: $(git log -1 --pretty=format:"%h - %s")"
                    else
                        echo "  Not a git repository"
                        fi
                        echo ""
                        
                        # Project structure
                        echo "📁 Project Structure:"
                        echo "-------------------"
                        FILES=$(find . -type f -not -path "./node_modules/*" -not -path "./.git/*" | wc -l)
                        DIRS=$(find . -type d -not -path "./node_modules/*" -not -path "./.git/*" | wc -l)
                        echo "  Files: $FILES"
                        echo "  Directories: $DIRS"
                        echo "  Largest file: $(find . -type f -not -path "./node_modules/*" -not -path "./.git/*" -exec du -h {} + 2>/dev/null | sort -rh | head -1 | cut -f2)"
                        echo ""
                        
                        # Security status
                        echo "🛡️  Security Status:"
                        echo "-----------------"
                        if command -v trivy &> /dev/null; then
                            echo "  Trivy: Available"
                            else
                                echo -e "  ${YELLOW}Trivy: Not installed${NC}"
                                fi
                                
                                if command -v shellcheck &> /dev/null; then
                                    echo "  ShellCheck: Available"
                                    else
                                        echo -e "  ${YELLOW}ShellCheck: Not installed${NC}"
                                        fi
                                        
                                        # Check for sensitive files (exclude known legitimate files and virtual env)
                                        SENSITIVE_FILES=$(find . -type f \( -name ".env" -o -name "*secret*" -o -name "*password*" -o -name "*key*" \) -not -path "./node_modules/*" -not -path "./.git/*" -not -path "./.venv/*" -not -path "./key_backups/*" -not -name "snowflake_rsa_key.*" -not -name "*key_rotation.py" -not -name "*.pyc" -not -name "*.pyo" 2>/dev/null)
                                        SENSITIVE_COUNT=$(echo "$SENSITIVE_FILES" | wc -l)
                                        
                                        # Check if any sensitive files are tracked by git
                                        TRACKED_SENSITIVE=$(git ls-files $SENSITIVE_FILES 2>/dev/null | wc -l)
                                        
                                        if [ "$TRACKED_SENSITIVE" -gt 0 ]; then
                                            echo -e "  ${RED}🚨 $TRACKED_SENSITIVE sensitive files tracked by git${NC}"
                                        elif [ "$SENSITIVE_COUNT" -gt 0 ]; then
                                            echo -e "  ${YELLOW}⚠️  $SENSITIVE_COUNT sensitive files (untracked)${NC}"
                                        else
                                            echo "  ✅ No sensitive files detected"
                                        fi
                                                echo ""
                                                
                                                # Recommendations
                                                echo "🎯 Recommendations:"
                                                echo "-----------------"
                                                [ ! -f ".github/workflows/ci.yml" ] && echo "  1. Add CI/CD workflow"
                                                [ ! -f "Dockerfile" ] && [ -f "package.json" ] && echo "  2. Consider containerizing with Docker"
                                                [ ! -f "README.md" ] && echo "  3. Add README documentation"
                                                [ ! -f ".gitignore" ] && echo "  4. Create .gitignore file"
                                                echo ""
                                                
                                                echo "📈 Run './codespace_validate.sh' for detailed validation"