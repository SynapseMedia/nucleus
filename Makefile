	export SHELL:=/bin/bash

PYTHON_MODULES = src
PYTHONPATH = .
VENV = .venv
PYTEST = env PYTHONPATH=${PYTHONPATH} PYTEST=1 ${VENV}/bin/py.test -c ./conftest.py --no-header -v
FLAKE8 = env PYTHONPATH=${PYTHONPATH} ${VENV}/bin/flake8 --config=.config/flake8.ini
COVERAGE = env PYTHONPATH=${PYTHONPATH} ${VENV}/bin/coverage
BLACKFIX = env PYTHONPATH=${PYTHONPATH} ${VENV}/bin/black
PYTHON = env PYTHONPATH=${PYTHONPATH} ${VENV}/bin/python
PIP = ${VENV}/bin/pip

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
		${PIP} install -q ${REQUIREMENTS}; \
	fi
bootstrap: venv requirements

fix-coding-style: bootstrap
	${BLACKFIX} ${PYTHON_MODULES}
check-coding-style: bootstrap
	${FLAKE8} ${PYTHON_MODULES}
test:
	${PYTEST} ${PYTHON_MODULES} --disable-pytest-warnings
test-coverage: check-coding-style test
	${COVERAGE} run --source=./src ${VENV}/bin/py.test
	${COVERAGE} report
	${COVERAGE} html
test-check:
	${PYTEST} ${PYTHON_MODULES}

.PHONY: default venv requirements bootstrap check-coding-style test test-coverage

