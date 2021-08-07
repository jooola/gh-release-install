.PHONY: setup format lint test run-example

SHELL = bash
CPU_CORES = $(shell nproc)

MODULE = gh_release_install
# POETRY = tools/bin/poetry
POETRY = tools/venv/bin/poetry

$(POETRY):
	mkdir -p tools
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py > tools/install-poetry.py
	POETRY_HOME=tools/ python3 tools/install-poetry.py --yes

setup: $(POETRY)
	$(POETRY) install

format:
	${POETRY} run black .
	${POETRY} run isort --profile black .

lint:
	${POETRY} run black . --diff --check
	${POETRY} run pylint ${MODULE} tests

test:
	${POETRY} run pytest -n ${CPU_CORES} --color=yes -v --cov=${MODULE} tests

run-example:
	${POETRY} run gh-release-install \
		'prometheus/prometheus' \
		'prometheus-{version}.linux-amd64.tar.gz' \
		--extract 'prometheus-{version}.linux-amd64/prometheus' \
		'./prometheus'

all: setup format lint test
