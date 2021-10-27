export SHELL:=/bin/bash

PYTHON_MODULES = src
PYTHONPATH = .
VENV = .venv
PYTEST = env PYTHONPATH=${PYTHONPATH} pytest -c ./conftest.py --no-header -v
FLAKE8 = env PYTHONPATH=${PYTHONPATH} flake8 --config=.config/flake8.ini
COVERAGE = env PYTHONPATH=${PYTHONPATH} coverage
BLACKFIX = env PYTHONPATH=${PYTHONPATH} black
PYTHON = env PYTHONPATH=${PYTHONPATH} python

VIRTUALENV := virtualenv
REQUIREMENTS := -r requirements.txt

default: check-coding-style

setup-env:
	virtualenv -q .venv
	python -m pip install --upgrade pip
	npm i
venv:
	test -d ${VENV} || ${VIRTUALENV} -q ${VENV}

requirements:
	@if [ -d wheelhouse ]; then \
		pip install -q --no-index --find-links=wheelhouse ${REQUIREMENTS}; \
	else \
		pip install -q ${REQUIREMENTS}; \
	fi
bootstrap: requirements setup-env venv

fix-coding-style: setup-env venv
	${BLACKFIX} ${PYTHON_MODULES}

check-coding-style: setup-env venv
	${FLAKE8} ${PYTHON_MODULES}

test: setup-env venv
	${PYTEST} ${PYTHON_MODULES} --disable-pytest-warnings

test-coverage: test
	${COVERAGE} run --source=./src ${VENV}/bin/py.test
	${COVERAGE} report
	${COVERAGE} html

test-check:
	${PYTEST} ${PYTHON_MODULES}

.PHONY: default venv requirements bootstrap check-coding-style test test-coverage

