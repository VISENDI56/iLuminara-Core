#!/bin/bash
# Quick setup for GitHub Codespace validation

echo "Setting up Enterprise Validation in GitHub Codespace..."

# Install essential tools
sudo apt-get update
sudo apt-get install -y \
    shellcheck \
        jq \
            tree \
                python3-pip \
                    npm \
                        golang

                        # Install security scanners
                        echo "Installing security scanners..."
                        pip3 install --user safety bandit semgrep
                        npm install -g npm-audit-ci

                        # Install Trivy
                        wget https://github.com/aquasecurity/trivy/releases/download/v0.45.1/trivy_0.45.1_Linux-64bit.deb
                        sudo dpkg -i trivy_0.45.1_Linux-64bit.deb
                        rm trivy_0.45.1_Linux-64bit.deb

                        # Create validation script
                        cat > validate.sh << 'SCRIPTEOF'
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
                        SCRIPTEOF

                        chmod +x validate.sh

                        echo "✅ Enterprise validation setup complete!"
                        echo "📋 Available commands:"
                        echo "   ./validate.sh      - Quick validation"
                        echo "   shellcheck *.sh    - Check shell scripts"
                        echo "   trivy fs .         - Security scan"
                        echo "   npm audit          - Node.js security audit"