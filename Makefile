.PHONY: check format lint test

check:
	ruff check
	ruff format --check
	mypy

format:
	ruff format

lint: format
	ruff check --fix

test:
	pytest
