	export SHELL:=/bin/bash

PYTHON_MODULES = src
PYTHONPATH = .
VENV = .venv
PYTEST = env PYTHONPATH=${PYTHONPATH} PYTEST=1 pytest -c ./conftest.py --no-header -v
FLAKE8 = env PYTHONPATH=${PYTHONPATH} flake8 --config=.config/flake8.ini
COVERAGE = env PYTHONPATH=${PYTHONPATH} coverage
BLACKFIX = env PYTHONPATH=${PYTHONPATH} black
PYTHON = env PYTHONPATH=${PYTHONPATH} python

VIRTUALENV := virtualenv
REQUIREMENTS := -r requirements.txt

default: check-coding-style

setup-env:
	pip install --upgrade pip
	pip install virtualenv
	virtualenv -q .venv

venv:
	test -d ${VENV} || ${VIRTUALENV} -q ${VENV}


requirements:
	@if [ -d wheelhouse ]; then \
		pip install -q --no-index --find-links=wheelhouse ${REQUIREMENTS}; \
	else \
		pip install -q ${REQUIREMENTS}; \
	fi

bootstrap: venv requirements

fix-coding-style: bootstrap
	${BLACKFIX} ${PYTHON_MODULES}

check-coding-style: bootstrap
	${FLAKE8} ${PYTHON_MODULES}

test: bootstrap
	${PYTEST} ${PYTHON_MODULES} --disable-pytest-warnings

test-coverage: test
	${COVERAGE} run --source=./src pytest
	${COVERAGE} report
	${COVERAGE} html

test-check:
	${PYTEST} ${PYTHON_MODULES}

.PHONY: default venv requirements bootstrap check-coding-style test test-coverage

