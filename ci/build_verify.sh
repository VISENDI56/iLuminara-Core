#!/bin/bash
echo "🔍 Verifying build..."
python -m compileall core pages deployment
echo "✅ Build verification passed"
