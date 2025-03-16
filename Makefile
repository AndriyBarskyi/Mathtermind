.PHONY: setup run clean test lint db-init db-seed db-reset db-migrate db-status help

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
	@echo "  make test       - Run tests"
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
	find . -name "*.pyc" -delete

# Test target
test:
	$(PYTHON) -m pytest

# Lint target
lint:
	$(PYTHON) -m flake8 src
	$(PYTHON) -m black --check src

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