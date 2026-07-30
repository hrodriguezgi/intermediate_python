.PHONY: help install dev lint format test clean docker-build docker-push deploy data-dict data-dict-app

help:
	@echo "Available commands:"
	@echo "  make install        - Install dependencies"
	@echo "  make dev            - Install development dependencies"
	@echo "  make lint           - Run linting checks"
	@echo "  make format         - Format code with black"
	@echo "  make type-check     - Run type checking"
	@echo "  make test           - Run tests"
	@echo "  make test-coverage  - Run tests with coverage"
	@echo "  make clean          - Clean build artifacts"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-test    - Test Docker image locally"
	@echo "  make docker-push    - Push Docker image to ECR"
	@echo "  make data-dict      - Generate data dictionary parquet files"
	@echo "  make data-dict-app  - Launch Streamlit data dictionary explorer"

install:
	uv sync

dev:
	uv sync --extra dev

lint:
	ruff check module_4_etl_pipelines/ tests/

format:
	black module_4_etl_pipelines/

type-check:
	mypy module_4_etl_pipelines/

test:
	pytest tests/ -v

test-coverage:
	pytest tests/ -v --cov=module_4_etl_pipelines --cov-report=html --cov-report=term

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.DS_Store" -delete
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov/ dist/ build/ *.egg-info/

docker-build:
	docker build -t data_engineering_etl:latest .

docker-test:
	docker run --rm \
		--env-file .env \
		-p 9000:8080 \
		data_engineering_etl:latest

all: clean install lint type-check test
