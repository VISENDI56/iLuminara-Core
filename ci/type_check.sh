#!/bin/bash
echo "🔍 Running type check..."
mypy core pages deployment
echo "✅ Type check passed"
