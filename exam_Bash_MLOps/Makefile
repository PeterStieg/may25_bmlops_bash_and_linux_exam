# Makefile for MLOps pipeline

.PHONY: setup install update-deps collect preprocess train tests clean

# Virtual environment activation
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/uv

setup:
	@echo "\n### 1. Setting up development environment...\n"
	cd scripts && bash setup.sh

# Install/update dependencies
install:
	@echo "\n### 2. Installing dependencies from requirements.txt\n"
	uv pip install -r requirements.txt

# Update requirements.txt from pyproject.toml
update-deps:
	@echo "\n### 3. Updating requirements.txt from pyproject.toml\n"
	uv pip compile pyproject.toml --output-file requirements.txt

# Start API
api-start:
	@echo "\n### 4. Starting API server\n"
	@cd .. && ./api >> exam_Bash_MLOps/logs/api.log 2>&1 & echo $$! > api.pid

# Your existing pipeline steps
collect:
	cd scripts && bash collect.sh
	@echo "\n\t5.1 Data collection completed\n"

preprocess:
	cd scripts && bash preprocessed.sh
	@echo "\n\t5.2 Data preprocessing completed\n"

train:
	cd scripts && bash train.sh
	@echo "\n\t5.3 Model training completed\n"

# Pipeline
pipeline: pipeline-start collect preprocess train tests pipeline-end

pipeline-start:
	@echo "\n### 5. Running pipeline\n"

pipeline-end:
	@echo "\n### 5. Pipeline completed\n"

tests:
	@echo "\n### 6. Running tests\n"
	pytest tests/test_collect.py && \
	pytest tests/test_preprocessed.py && \
	pytest tests/test_model.py

# Stop API
api-stop:
	@echo "\n### 7. Stopping API server\n"
	@if [ -f api.pid ]; then \
	kill `cat api.pid` && rm api.pid; \
	echo "API stopped successfully"; \

clean:
	@echo "\n### 8. Cleaning up\n"
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf *.pyc

# Command to run the Makefile
bash: setup install update-deps api-start pipeline tests api-stop clean