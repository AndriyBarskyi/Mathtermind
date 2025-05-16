.PHONY: setup run clean clean-logs test test-unit test-service test-specific lint db-init db-seed db-reset db-migrate db-status help

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON = python
VENV = venv
VENV_BIN = $(VENV)/bin
VENV_PYTHON = $(VENV_BIN)/python
DB_MANAGE = $(PYTHON) db_manage.py

# Help target
help:
	@echo "Mathtermind Makefile"
	@echo "===================="
	@echo "Available commands:"
	@echo "  make setup      - Set up the project (create venv, install dependencies, init db)"
	@echo "  make run        - Run the application"
	@echo "  make clean      - Clean up temporary files and caches"
	@echo "  make clean-logs - Clean up error logs in logs/error_reports directory"
	@echo "  make test       - Run all tests"
	@echo "  make test-unit  - Run unit tests only"
	@echo "  make test-service SERVICE=<service_name> - Run tests for specific service (e.g., cs_tools)"
	@echo "  make test-specific PATH=<path> - Run specific test file or directory"
	@echo "  make lint       - Run linting tools"
	@echo "  make db-init    - Initialize the database"
	@echo "  make db-seed    - Seed the database with sample data"
	@echo "  make db-reset   - Reset the database"
	@echo "  make db-migrate - Run database migrations"
	@echo "  make db-status  - Show database migration status"

# Setup target
setup:
	$(PYTHON) setup.py

# Run target
run:
	$(PYTHON) main.py

# Clean target
clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf src/*/__pycache__
	rm -rf src/*/*/__pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -name "*.pyc" -delete

# Clean logs target
clean-logs:
	find logs/error_reports -name "*.json" -type f -delete
	@echo "Error logs cleaned successfully"

# Test targets
test:
	$(PYTHON) -m pytest

# Run only unit tests
test-unit:
	$(PYTHON) -m pytest -m unit

# Run tests for a specific service
test-service:
	$(PYTHON) -m pytest src/tests/services/test_$(SERVICE)_service.py -v

# Run a specific test file or directory
test-specific:
	$(PYTHON) -m pytest $(PATH) -v

# Lint target
lint:
	$(PYTHON) -m flake8 src
	$(PYTHON) -m black --check src

# Coverage target
coverage:
	$(PYTHON) -m pytest --cov=src --cov-report=term-missing --cov-report=html

# Database targets
db-init:
	$(DB_MANAGE) init

db-seed:
	$(DB_MANAGE) seed

db-reset:
	$(DB_MANAGE) reset

db-migrate:
	$(DB_MANAGE) migrate

db-status:
	$(DB_MANAGE) status 