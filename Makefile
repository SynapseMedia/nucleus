
export SHELL:=/bin/bash


PYTHON_MODULES = nucleus/
PYTHONPATH = .
VENV = .venv
PYTYPE = env PYTHONPATH=${PYTHONPATH} ${VENV}/bin/pyright 
PYTEST = env PYTHONPATH=${PYTHONPATH} PYTEST=1 ${VENV}/bin/py.test -c pytest.ini --no-header --durations=5 --disable-pytest-warnings -v  
FLAKE8 = env PYTHONPATH=${PYTHONPATH} ${VENV}/bin/flake8 --config=flake8.ini 
COVERAGE = env PYTHONPATH=${PYTHONPATH} ${VENV}/bin/coverage 
BLACKFIX = env PYTHONPATH=${PYTHONPATH} ${VENV}/bin/black
AUTOPEP8 = env PYTHONPATH=${PYTHONPATH} ${VENV}/bin/autopep8
PYTHON = env PYTHONPATH=${PYTHONPATH} ${VENV}/bin/python3
PIP = ${VENV}/bin/pip3

DEFAULT_PYTHON := /usr/bin/python3
VIRTUALENV := /usr/bin/virtualenv
REQUIREMENTS := -r requirements.txt

default: check-coding-style

setup-env:
	virtualenv --python=python3 -q .venv
	python3 -m pip install --upgrade pip
venv:
	test -d ${VENV} || ${VIRTUALENV} -p ${DEFAULT_PYTHON} -q ${VENV}

requirements:
	@if [ -d wheelhouse ]; then \
		${PIP} install -q --no-index --find-links=wheelhouse ${REQUIREMENTS}; \
	else \
		${PIP} install --no-cache-dir --force-reinstall ${REQUIREMENTS}; \
	fi

	npm i

bootstrap: setup-env venv requirements

code-fix: venv
	${BLACKFIX} ${PYTHON_MODULES}
	${AUTOPEP8} --in-place --aggressive --aggressive --recursive -v ./${PYTHON_MODULES}

code-check: venv
	${FLAKE8} ${PYTHON_MODULES}

type-check: venv
	${PYTYPE} ${PYTHON_MODULES}/

test: venv
	${PYTEST} ${PYTHON_MODULES}/tests/$(filter-out $@,$(MAKECMDGOALS))

test-debug: venv
	${PYTEST} --pdb ${PYTHON_MODULES}/tests/$(filter-out $@,$(MAKECMDGOALS))

test-coverage: 
	${PYTEST} --cov-report term --cov-report  xml:coverage.xml --cov=src

test-check:
	${PYTEST} ${PYTHON_MODULES}


# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
