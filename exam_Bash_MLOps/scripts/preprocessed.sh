#!/bin/bash
# =============================================================================
# This script preprocessed.sh runs the program src/preprocessed.py
# and logs the execution details in the log file
# logs/preprocessed.logs.
# =============================================================================

# Activate the virtual environment
cd .. && source venv/bin/activate

# Run the preprocessing script
#cd ../src && python3 preprocessed.py

echo "Script started in: $(pwd)"
echo "Script location: $(dirname "$0")"
echo "Available files here:"
ls -la