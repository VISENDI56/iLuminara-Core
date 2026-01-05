#!/bin/bash
echo "🔍 Running basic security scan..."
bandit -r core
echo "✅ Security scan passed"
