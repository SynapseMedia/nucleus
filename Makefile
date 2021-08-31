PYTHON_MODULES := src
PYTHONPATH := .
VENV := .venv
PYTEST := env PYTHONPATH=$(PYTHONPATH) PYTEST=1 $(VENV)/bin/py.test
FLAKE8 := env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/flake8
PEP8FIX := env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/autopep8 -i -r -a
BLACKFIX := env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/black
PYLINT := env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/pylint --disable=I0011 --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"
PYTHON := env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/python
PIP := $(VENV)/bin/pip

DEFAULT_PYTHON := /usr/bin/python3
VIRTUALENV := /usr/bin/virtualenv
REQUIREMENTS := -r requirements.txt

default: check-coding-style

setup-env:
	virtualenv --python=python3 -q .venv
venv:
	test -d $(VENV) || $(VIRTUALENV) -p $(DEFAULT_PYTHON) -q $(VENV)
requirements:
	@if [ -d wheelhouse ]; then \
		$(PIP) install -q --no-index --find-links=wheelhouse $(REQUIREMENTS); \
	else \
		$(PIP) install -q $(REQUIREMENTS); \
	fi
bootstrap: venv requirements

fix-coding-style: bootstrap
	$(PEP8FIX) $(PYTHON_MODULES)
	$(BLACKFIX) $(PYTHON_MODULES)
check-coding-style: bootstrap
	$(FLAKE8) $(PYTHON_MODULES)
	$(PYLINT) -E $(PYTHON_MODULES)
pylint-full: check-coding-style
	$(PYLINT) $(PYTHON_MODULES)
test: check-coding-style
	$(PYTEST) $(PYTHON_MODULES)
test-check:
	$(PYTEST) $(PYTHON_MODULES)

.PHONY: default venv requirements bootstrap check-coding-style pylint-full test check