#!/bin/bash
# -----------------------------------------------------------------------------
# This script train.sh runs the Python program src/train.py.
# This program trains a prediction model and saves the final model
# in the model/ directory. The script also logs all execution details
# in the file logs/train.logs.
# -----------------------------------------------------------------------------

# Activate the virtual environment
source ../venv/bin/activate

# Run the preprocessing script
python3 ../src/train.py
