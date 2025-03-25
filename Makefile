.phony: format lint run test docker.build docker.build.quite docker.run export_deps build upload

export_deps:
	@echo "Make: Exporting dependencies..."
	@poetry export --without-hashes --format=requirements.txt > requirements.txt

format:
	@echo "Make: Running formatters..."
	@black src
	@isort src

lint: format
	@echo "Make: Running linters..."
	@ruff check src

run:
	@echo "Make: Running the application..."
	@python src/package.py

test:
	@echo "Make: Running tests..."
	@python -m pytest .

test_coverage:
	@echo "Make: Running tests with coverage..."
	@python -m pytest --cov=src --cov-report=term-missing .

docker.build: lint
	@echo "Make: Building a docker image... (Might be minutes)"
	@docker build -t package:dev .

docker.build.quite: lint
	@echo "Make: Building a docker image... (Might be minutes)"
	@docker build -q -t package:dev .

docker.run: docker.build.quite
	@echo "Make: Running docker container..."
	@docker run -p 8000:8000 -v $(PWD):/app package:dev run

build:
	@echo "Make: Building package..."
	@python3 -m pip install build
	@python3 -m build --wheel

upload: build
	@echo "Make: Uploading package..."
	@twine upload dist/*
	@rm -rf dist
	@rm -rf build
	@rm -rf *.egg-info
	@rm -rf .pytest_cache
	@rm -rf .coverage
	@rm -rf .eggs
	@rm -rf .tox
