.PHONY: install test lint format type-check ci docker-build

install:
	python -m pip install -e .[dev]

test:
	pytest -q

lint:
	ruff check .
	black --check .

type-check:
	mypy src

format:
	black .
	docs:
	python -m bioml_workbench --show-config

ci: lint type-check test

docker-build:
	docker build -t bioml-workbench:latest .
