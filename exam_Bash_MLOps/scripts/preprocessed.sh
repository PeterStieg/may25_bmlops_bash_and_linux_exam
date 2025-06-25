#!/bin/bash
# =============================================================================
# This script preprocessed.sh runs the program src/preprocessed.py
# and logs the execution details in the log file
# logs/preprocessed.logs.
# =============================================================================

# Activate the virtual environment
source venv/bin/activate

# Run the preprocessing script
python3 src/preprocessed.py