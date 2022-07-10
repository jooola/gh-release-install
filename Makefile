.PHONY: setup format lint test e2e run-example

SHELL = bash
CPU_CORES = $(shell nproc)

MODULE = gh_release_install

install-poetry:
	curl -sSL https://install.python-poetry.org | python3 -

install:
	poetry install

format:
	poetry run black .
	poetry run isort --profile black .

lint:
	poetry run black . --diff --check
	poetry run pylint $(MODULE) tests
	poetry run mypy $(MODULE) tests || true

test:
	poetry run pytest -n $(CPU_CORES) --color=yes -v --cov=$(MODULE) tests

e2e:
	poetry run pytest -n $(CPU_CORES) --color=yes -v --cov=$(MODULE) e2e

run-example:
	poetry run gh-release-install -vv \
		'grafana/loki' \
		'loki-linux-amd64.zip' --extract 'loki-linux-amd64' \
		'./loki' \
		--version 'latest' --version-file '{destination}.version'

ci-publish:
	poetry publish --no-interaction --build

all: install format lint test
