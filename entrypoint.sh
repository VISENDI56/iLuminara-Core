#!/bin/bash

echo "╔════════════════════════════════════════════════════════╗"
echo "║   iLuminara-Core: Container Initialization            ║"
echo "╚════════════════════════════════════════════════════════╝"

# Set default environment variables
export ILUMINARA_MODE=${ILUMINARA_MODE:-test}
export ILUMINARA_CONTEXT=${ILUMINARA_CONTEXT:-131072}
export PYTHONPATH=/app

echo "Configuration:"
echo "  Mode: $ILUMINARA_MODE"
echo "  Context: $ILUMINARA_CONTEXT tokens"
echo "  Python Path: $PYTHONPATH"
echo ""

# Validate installation
echo "Validating installation..."
python -c "
import sys
print(f'Python: {sys.version}')

try:
    import torch
    print(f'PyTorch: {torch.__version__}')
except ImportError:
    print('PyTorch: Not installed')

try:
    import streamlit
    print(f'Streamlit: {streamlit.__version__}')
except ImportError:
    print('Streamlit: Not installed')
"

echo ""
echo "Starting iLuminara Sovereign OS..."
echo "Access dashboard at: http://localhost:8501"
echo ""

# Execute the command
exec "$@"
