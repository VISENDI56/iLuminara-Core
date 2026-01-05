# iLuminara Polyglot Build System

.PHONY: test-all test-python test-dart test-infra clean

test-all: test-python test-dart test-infra

test-python:
@echo "🔍 Testing Core IMS Kernel (Python)..."
cd core && pytest

test-dart:
@echo "📱 Testing Mobile Agents (Dart/Flutter)..."
cd mobile && flutter test

test-infra:
@echo "🛡️  Auditing Infrastructure Hardening (Shell)..."
bash infra/hardening/audit_configs.sh

clean:
find . -type d -name "__pycache__" -exec rm -rf {} +
cd mobile && flutter clean
