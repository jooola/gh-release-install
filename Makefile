.PHONY: install format lint test e2e run-example

SHELL = bash
CPU_CORES = $$(( $(shell nproc) > 4 ? 4 : $(shell nproc) ))

all: install format lint test

install-poetry:
	curl -sSL https://install.python-poetry.org | python3 -

POETRY_VIRTUALENVS_IN_PROJECT = true

INSTALL_STAMP := .installed
install: $(INSTALL_STAMP)
$(INSTALL_STAMP):
	poetry install
	touch $(INSTALL_STAMP)

format: install
	poetry run black .
	poetry run isort --profile black .

lint: install
	poetry run black . --diff --check
	poetry run pylint gh_release_install tests
	poetry run mypy gh_release_install tests

test: install
	poetry run pytest -n $(CPU_CORES) --color=yes -v --cov=gh_release_install tests

e2e: install
	poetry run pytest -n $(CPU_CORES) --color=yes -v --cov=gh_release_install e2e

examples: install
	poetry run ./examples.sh

ci-publish: install
	poetry publish --no-interaction --build
