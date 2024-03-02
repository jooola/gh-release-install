.PHONY: install format lint test e2e run-example

SHELL = bash
CPU_CORES = $$(( $(shell nproc) > 4 ? 4 : $(shell nproc) ))

all: install format lint test

install-poetry:
	curl -sSL https://install.python-poetry.org | python3 -

export POETRY_VIRTUALENVS_IN_PROJECT = true

install: .venv
.venv:
	poetry install

format: .venv
	poetry run black .
	poetry run isort .

lint: .venv
	poetry run black . --diff --check
	poetry run pylint gh_release_install tests
	poetry run mypy gh_release_install tests

test: .venv
	poetry run pytest -n $(CPU_CORES) --color=yes -v --cov=gh_release_install tests

e2e: .venv
	poetry run pytest -n $(CPU_CORES) --color=yes -v --cov=gh_release_install e2e

examples: .venv
	poetry run ./examples.sh

ci-publish: .venv
	poetry publish --no-interaction --build
