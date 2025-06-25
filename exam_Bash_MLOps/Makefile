# Makefile for MLOps pipeline

.PHONY: setup install update-deps collect preprocess train tests clean

# Virtual environment activation
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/uv pip

setup:
	@echo "1. Setting up development environment..."
	cd scripts && bash setup.sh

# Install/update dependencies
install:
	@echo "2. Installing dependencies from requirements.txt"
	uv pip install -r requirements.txt

# Update requirements.txt from pyproject.toml
update-deps:
	@echo "3. Updating requirements.txt from pyproject.toml"
	uv pip compile pyproject.toml --output-file requirements.txt

# Start API
api-start:
	@echo "4. Starting API server..."
	@cd .. && ./api >> exam_Bash_MLOps/logs/api.log 2>&1 & echo $$! > api.pid

# Your existing pipeline steps
collect:
	cd scripts && bash collect.sh
	@echo "\t5.1 Data collection completed."

preprocess:
	cd scripts && bash preprocessed.sh
	@echo "\t5.2 Data preprocessing completed."

train:
	cd scripts && bash train.sh
	@echo "\t5.3 Model training completed."

# Pipeline
pipeline: pipeline-start collect preprocess train tests pipeline-end

pipeline-start:
	@echo "5. Running pipeline..."

pipeline-end:
	@echo "5. Full pipeline completed successfully!"

tests:
	@echo "5. Running tests"
	pytest tests/test_collect.py && \
	pytest tests/test_preprocessed.py && \
	pytest tests/test_model.py

# Stop API
api-stop:
	@echo "6. Stopping API server..."
	@if [ -f api.pid ]; then \
	kill `cat api.pid` && rm api.pid; \
	echo "API stopped successfully"; \

clean:
	@echo "7. Cleaning up"
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf *.pyc

# Command to run the Makefile
bash: setup install update-deps api-start pipeline tests api-stop clean