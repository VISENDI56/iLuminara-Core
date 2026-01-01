#!/bin/bash
echo "🛡️  Enterprise Validation Quick Check"
echo "==================================="
echo "Date: $(date)"
echo ""

# Basic checks
echo "1. System Information:"
echo "   OS: $(lsb_release -d 2>/dev/null | cut -f2 || uname -a)"
echo "   Node: $(node --version 2>/dev/null || echo 'Not installed')"
echo "   Python: $(python3 --version 2>/dev/null || echo 'Not installed')"
echo "   Go: $(go version 2>/dev/null || echo 'Not installed')"
echo ""

echo "2. Security Tools:"
echo "   Trivy: $(trivy --version 2>/dev/null | head -1 || echo 'Not installed')"
echo "   ShellCheck: $(shellcheck --version 2>/dev/null | head -1 || echo 'Not installed')"
echo "   Safety: $(safety --version 2>/dev/null || echo 'Not installed')"
echo ""

echo "3. Quick Security Scan:"
find . -name "*.sh" -exec shellcheck {} \; 2>/dev/null | head -3
echo ""

echo "✅ Setup complete! Run './validate.sh' for quick validation."