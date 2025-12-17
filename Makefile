# Makefile for F1 Racing Game
# Following Python project best practices

.PHONY: help install test lint format clean run setup dev-setup

# Default target
help:
	@echo "🏎️  F1 Racing Game - Development Commands"
	@echo ""
	@echo "Setup Commands:"
	@echo "  setup       Set up virtual environment and install dependencies"
	@echo "  install     Install/update dependencies"
	@echo ""
	@echo "Development Commands:"
	@echo "  run         Run the game"
	@echo "  test        Run all tests"
	@echo "  lint        Run code linting"
	@echo "  format      Format code with black"
	@echo "  dev-setup   Setup development environment with pre-commit hooks"
	@echo ""
	@echo "Maintenance Commands:"
	@echo "  clean       Clean up generated files"
	@echo "  clean-all   Clean everything including virtual environment"

# Setup virtual environment
setup:
	@echo "🔧 Setting up virtual environment..."
	./setup_env.sh

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	@if [ ! -d "venv" ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@source venv/bin/activate && pip install --upgrade pip
	@source venv/bin/activate && pip install -r requirements.txt

# Run the game
run:
	@echo "🎮 Starting F1 Racing Game..."
	@if [ ! -d "venv" ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@source venv/bin/activate && cd F1RacerGame && python index.py

# Run tests
test:
	@echo "🧪 Running tests..."
	@if [ ! -d "venv" ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@source venv/bin/activate && python -m pytest tests/ -v

# Run linting
lint:
	@echo "🔍 Running code linting..."
	@if [ ! -d "venv" ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@source venv/bin/activate && flake8 F1RacerGame/ tests/ --max-line-length=100 --ignore=E203,W503

# Format code
format:
	@echo "✨ Formatting code..."
	@if [ ! -d "venv" ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@source venv/bin/activate && black F1RacerGame/ tests/ --line-length=100

# Development setup with additional tools
dev-setup: setup
	@echo "🛠️  Setting up development environment..."
	@source venv/bin/activate && pip install pre-commit mypy
	@echo "✅ Development environment ready!"

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".coverage" -delete
	@find . -name "*.log" -delete
	@rm -rf F1RacerGame/logs/
	@echo "✅ Cleanup complete!"

# Clean everything including virtual environment
clean-all: clean
	@echo "🗑️  Removing virtual environment..."
	@rm -rf venv/
	@echo "✅ Complete cleanup finished!"

# Check environment status
status:
	@echo "📊 Environment Status:"
	@if [ -d "venv" ]; then \
		echo "✅ Virtual environment: Present"; \
		source venv/bin/activate && echo "🐍 Python version: $$(python --version)"; \
		source venv/bin/activate && echo "📦 Installed packages: $$(pip list | wc -l) packages"; \
	else \
		echo "❌ Virtual environment: Missing"; \
	fi
	@if [ -f "requirements.txt" ]; then \
		echo "✅ Requirements file: Present"; \
	else \
		echo "❌ Requirements file: Missing"; \
	fi