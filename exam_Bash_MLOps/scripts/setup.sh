#!/bin/bash
# setup.sh - System dependencies and Python environment setup

# Update package list
sudo apt-get update

# Install system dependencies
sudo apt-get install -y python3-dev python3-venv build-essential

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH for current session
export PATH="$HOME/.local/bin:$PATH"

# Go to root directory to create venv there
cd ..

# Create virtual environment with uv (much faster than python3 -m venv)
uv venv venv --python 3.12

# Activate the virtual environment
source venv/bin/activate

# Install dependencies using uv (much faster than pip)
uv pip install -r requirements.txt

# Create directories
mkdir -p logs data/processed model