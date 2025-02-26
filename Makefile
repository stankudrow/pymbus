.PHONY: check lint test

check:
	ruff check
	ruff format --check

lint:
	ruff format
	ruff check --fix

test:
	pytest
