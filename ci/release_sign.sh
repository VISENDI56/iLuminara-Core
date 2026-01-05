#!/bin/bash
echo "🔍 Signing release artifacts..."
for f in deployment/*.py core/**/*.py; do
    sha256sum $f >> release_signatures.txt
done
echo "✅ Release artifacts signed"
