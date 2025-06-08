.PHONY: help install dev test lint format clean run activate

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	poetry install

dev:  ## Install development dependencies
	poetry install --with dev

activate:  ## Show command to activate virtual environment
	@echo "To activate the virtual environment, run:"
	@echo "source .venv/bin/activate"
	@echo ""
	@echo "Your prompt will show (train-ai) when activated"

test:  ## Run tests
	poetry run pytest

lint:  ## Run linting
	poetry run flake8 app tests
	poetry run mypy app

format:  ## Format code
	poetry run black app tests
	poetry run isort app tests

clean:  ## Clean cache and temporary files
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

run:  ## Run the development server
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

deploy:  ## Deploy using gunicorn
	poetry run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

setup:  ## Initial project setup
	poetry install
	pre-commit install 