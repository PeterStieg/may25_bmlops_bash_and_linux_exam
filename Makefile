# Makefile for exam_Bash_MLOps

# Variables (optional but useful)
PYTHON = python3
PIP = pip3
SCRIPT = main.py
REQUIREMENTS = requirements.txt

# Default target (runs when you just type 'make')
.DEFAULT_GOAL := help

# Help target - shows available commands
help:
	@echo "Available commands:"
	@echo "  make install   - Install dependencies"

# Install updates as well as system Ubuntu and Python dependencies
install:
	sudo apt-get update
	sudo apt-get upgrade -y
	sudo apt-get install curl -y
	# $(PIP) install -r $(REQUIREMENTS)
