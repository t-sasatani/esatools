.PHONY: check format

check:
	poetry run ruff check esatools
	poetry run isort --check-only esatools
	poetry run black --check esatools

format:
	poetry run ruff check --fix esatools
	poetry run isort esatools
	poetry run black esatools