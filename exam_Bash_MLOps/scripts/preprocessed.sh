#!/bin/bash
# =============================================================================
# This script preprocessed.sh runs the program src/preprocessed.py
# and logs the execution details in the log file
# logs/preprocessed.logs.
# =============================================================================

# Activate the virtual environment
source venv/bin/activate

# Run the preprocessing script
#cd src && python3 preprocessed.py

echo "=== DEBUGGING preprocessed.sh ==="
echo "Script started in: $(pwd)"
echo "Script location: $(dirname "$0")"
echo "Available files here:"
ls -la
echo "Looking for src directory:"
ls -la src/ 2>/dev/null || echo "src/ directory not found"
echo "Looking for preprocessed.py:"
find . -name "preprocessed.py" -type f
echo "=== END DEBUGGING ==="