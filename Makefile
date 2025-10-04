.PHONY: install format lint test e2e examples

SHELL = bash

all: install format lint test

install: venv
venv:
	python3 -m venv venv
	venv/bin/pip install -e .[dev]

format: venv
	venv/bin/black .
	venv/bin/isort .

lint: venv
	venv/bin/black . --diff --check
	venv/bin/pylint gh_release_install tests
	venv/bin/mypy gh_release_install tests

test: venv
	venv/bin/pytest --color=yes -v --cov=gh_release_install tests

e2e: venv
	venv/bin/pytest --color=yes -v --cov=gh_release_install e2e

examples: venv
	source venv/bin/activate; ./examples.sh
