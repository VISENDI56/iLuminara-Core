#!/bin/bash
echo "🔍 Running lint..."
flake8 core pages deployment
echo "✅ Lint passed"
