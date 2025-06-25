#!/bin/bash
# -----------------------------------------------------------------------------
# This script train.sh runs the Python program src/train.py.
# This program trains a prediction model and saves the final model
# in the model/ directory. The script also logs all execution details
# in the file logs/train.logs.
# -----------------------------------------------------------------------------


# Activate the virtual environment
cd .. && source venv/bin/activate

# Run the training script
cd ../src/ && python3 train.py