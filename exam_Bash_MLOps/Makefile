# Makefile for MLOps pipeline

# Force make to use bash instead of sh
SHELL := /bin/bash

.PHONY: setup install update-deps collect preprocess train tests clean

# Virtual environment activation
VENV = venv
PYTHON = $(VENV)/bin/python
UV = $(VENV)/bin/uv

setup:
	@echo "### 1. Setting up development environment"
	cd scripts && bash setup.sh

# Install/update dependencies
install:
	@echo "### 2. Installing dependencies from requirements.txt"
	source $(VENV)/bin/activate && uv pip install -r requirements.txt

# Update requirements.txt from pyproject.toml
update-deps:
	@echo "### 3. Updating requirements.txt from pyproject.toml"
	source $(VENV)/bin/activate && uv pip compile pyproject.toml --output-file requirements.txt

# Start API
api-start:
	@echo "### 4. Starting API server"
	@cd .. && ./api >> exam_Bash_MLOps/logs/api.log 2>&1 & echo $$! > api.pid

# Pipeline steps
collect:
	cd scripts && bash collect.sh
	@echo "### 5.1 Data collection completed"

preprocess:
	cd scripts && bash preprocessed.sh
	@echo "### 5.2 Data preprocessing completed"

train:
	cd scripts && bash train.sh
	@echo "### 5.3 Model training completed"

# Pipeline
pipeline: pipeline-start collect preprocess train tests pipeline-end

pipeline-start:
	@echo "### 5. Pipeline started"

pipeline-end:
	@echo "### 5. Pipeline completed"

tests:
	@echo "### 6. Running tests"
	source $(VENV)/bin/activate && pytest tests/test_collect.py && \
	pytest tests/test_preprocessed.py && \
	pytest tests/test_model.py

# Stop API
api-stop:
	@echo "### 7. Stopping API server"
	@if [ -f api.pid ]; then \
	kill `cat api.pid` && rm api.pid; \
	echo "API stopped successfully"; \
	fi

# Clean up environment
clean:
	@echo "### 8. Cleaning up"
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf *.pyc

# Command to run the Makefile
bash: setup install update-deps api-start pipeline tests api-stop clean