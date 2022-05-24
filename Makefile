export SHELL:=/bin/bash

PYTHON_MODULES = src
PYTHONPATH = .
VENV = .venv
PYTEST = env PYTHONPATH=${PYTHONPATH} PYTEST=1 ${VENV}/bin/py.test -c pytest.ini --no-header -v 
FLAKE8 = env PYTHONPATH=${PYTHONPATH} ${VENV}/bin/flake8 --config=.config/flake8.ini
COVERAGE = env PYTHONPATH=${PYTHONPATH} ${VENV}/bin/coverage
BLACKFIX = env PYTHONPATH=${PYTHONPATH} ${VENV}/bin/black
PYTHON = env PYTHONPATH=${PYTHONPATH} ${VENV}/bin/python
PIP = ${VENV}/bin/pip3

DEFAULT_PYTHON := /usr/bin/python3
VIRTUALENV := /usr/bin/virtualenv
REQUIREMENTS := -r requirements.txt

default: check-coding-style

setup-env:
	virtualenv --python=python3 -q .venv
	python -m pip install --upgrade pip
	npm i
venv:
	test -d ${VENV} || ${VIRTUALENV} -p ${DEFAULT_PYTHON} -q ${VENV}

requirements:
	@if [ -d wheelhouse ]; then \
		${PIP} install -q --no-index --find-links=wheelhouse ${REQUIREMENTS}; \
	else \
		${PIP} install --no-cache-dir --force-reinstall ${REQUIREMENTS}; \
	fi

bootstrap: setup-env venv requirements

fix-coding-style: venv
	${BLACKFIX} ${PYTHON_MODULES}
check-coding-style: venv
	${FLAKE8} ${PYTHON_MODULES}

test-core:
	${PYTEST} ${PYTHON_MODULES}/core --disable-pytest-warnings

test:
	${PYTEST} ${PYTHON_MODULES} --disable-pytest-warnings

test-coverage-core: check-coding-style test-core
	${COVERAGE} run --source=./src/core ${VENV}/bin/py.test
	${COVERAGE} report

test-coverage: test-coverage-core
	${COVERAGE} run --source=./src ${VENV}/bin/py.test
	${COVERAGE} report
	
test-coverage-html: test-coverage
	${COVERAGE} html
	
test-check:
	${PYTEST} ${PYTHON_MODULES}

.PHONY: default venv requirements bootstrap check-coding-style test test-coverage

