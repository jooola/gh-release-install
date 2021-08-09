.PHONY: setup format lint test e2e run-example

SHELL = bash
CPU_CORES = $(shell nproc)

MODULE = gh_release_install

POETRY_HOME = .poetry
POETRY = $(POETRY_HOME)/venv/bin/poetry

$(POETRY):
	mkdir -p $(POETRY_HOME)
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py > $(POETRY_HOME)/install-poetry.py
	POETRY_HOME=$(POETRY_HOME) python3 $(POETRY_HOME)/install-poetry.py --yes

setup: $(POETRY)
	$(POETRY) install

format:
	$(POETRY) run black .
	$(POETRY) run isort --profile black .

lint:
	$(POETRY) run black . --diff --check
	$(POETRY) run pylint $(MODULE) tests
	$(POETRY) run mypy $(MODULE) tests || true

test:
	$(POETRY) run pytest -n $(CPU_CORES) --color=yes -v --cov=$(MODULE) tests

e2e:
	$(POETRY) run pytest -n $(CPU_CORES) --color=yes -v --cov=$(MODULE) e2e

run-example:
	$(POETRY) run gh-release-install -vv \
		'grafana/loki' \
		'loki-linux-amd64.zip' --extract 'loki-linux-amd64' \
		'./loki' \
		--version 'latest' --version-file '{destination}.version'

ci-publish:
	$(POETRY) publish --no-interaction --build

all: setup format lint test
