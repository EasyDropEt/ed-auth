.phony: format lint run test docker.build docker.build.quite docker.run export_deps

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
	@python package.py

test:
	@echo "Make: Running tests..."
	@python -m pytest .

docker.build: lint
	@echo "Make: Building a docker image... (Might be minutes)"
	@docker build -t package:dev .

docker.build.quite: lint
	@echo "Make: Building a docker image... (Might be minutes)"
	@docker build -q -t package:dev .

docker.run: docker.build.quite
	@echo "Make: Running docker container..."
	@docker run -p 8000:8000 -v $(PWD):/app package:dev run
