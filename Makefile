.DEFAULT_GOAL := all
sources = nucleus

.PHONY: .pdm  ## Check that PDM is installed
.pdm:
	@pdm -V || echo 'Please install PDM: https://pdm.fming.dev/latest/\#installation'


.PHONY: install  ## Install the package, dependencies, and pre-commit for local development
install: .pdm 
	pdm install --group :all

.PHONY: refresh-lockfiles  ## Sync lockfiles with requirements files.
refresh-lockfiles: .pdm
	pdm lock --refresh --dev --group :all

.PHONY: test  ## Run all tests, skipping the type-checker integration tests
test: .pdm
	pdm run coverage run -m pytest 

.PHONY: debug  ## Run all tests, skipping the type-checker integration tests
debug: 
	pdm run coverage run -m pytest  --pdb

.PHONY: testcov  ## Run tests and generate a coverage report, skipping the type-checker integration tests
testcov: test
	@echo "building coverage html"
	@pdm run coverage html
	@echo "building coverage lcov"
	@pdm run coverage lcov

.PHONY: codespell  ## Use Codespell to do spellchecking
codespell: .pdm
	pdm run codespell $(sources)

.PHONY: format  ## Auto-format python source files
format: .pdm
	pdm run black  $(sources)
	pdm run ruff --fix $(sources)

.PHONY: lint  ## Lint python source files
lint: .pdm
	pdm run ruff $(sources)
	pdm run black --exclude 'tests' $(sources) --check --diff

.PHONY: pyright  ## Run the pyright integration tests
pyright: .pdm
	pdm run pyright

.PHONY: test  ## Run all tests, skipping the type-checker integration tests
publish: .pdm
	pdm publish

.PHONY: clean  ## Clear local caches and build artifacts
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]'`
	rm -f `find . -type f -name '*~'`
	rm -f `find . -type f -name '.*~'`
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf dist
	rm -rf coverage.lcov
	rm -rf site
	rm -rf docs/_build
	rm -rf docs/.changelog.md docs/.version.md docs/.tmp_schema_mappings.html
	rm -rf fastapi/test.db
	rm -rf coverage.xml
	
.PHONY: docs  ## Generate the docs
docs:
	pdm run mkdocs build
	

.PHONY: all  ## Run the standard set of checks performed in CI
all: lint pyright codespell test
