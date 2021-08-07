.PHONY: lint test

SHELL := bash
CPU_CORES := $(shell nproc)

MODULE := gh_release_install

setup:
	poetry install

lint:
	poetry run pylint ${MODULE} tests

format:
	poetry run black .
	poetry run isort --profile black .

test:
	poetry run pytest -n ${CPU_CORES} --color=yes -v --cov=${MODULE} tests

run-example:
	poetry run gh-release-install \
		'prometheus/prometheus' \
		'prometheus-{version}.linux-amd64.tar.gz' \
		--extract 'prometheus-{version}.linux-amd64/prometheus' \
		'./prometheus'

all: lint test
