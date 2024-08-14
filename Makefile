SHELL := bash
PYTHON := python3
RUFF := ruff

script_dir := $(shell readlink -e .)
APP_DIR := $(shell readlink -e "$(script_dir)")
TARGET_MODULE := valory_task
TARGETS := valory_task

.PHONY: all test lint lint_fix compile_all python_import non_final_globals unreasonable_globals ruff flake8 pylint mypy vulture shellcheck shellcheck_makefile validate_pyproject

all: lint test


test:
	$(PYTHON) -m unittest -v


lint_fix:
	$(RUFF) check --fix $(TARGETS)

compile_all:
	export PYTHONWARNINGS='ignore,error:::$(TARGET_MODULE)[.*]'
	# Running python compile:
	$(PYTHON) -O -m compileall $(TARGETS) \
	| (\
		grep -v -e '^Listing' -e '^Compiling' || true \
	)
	# :: python compile passed ::

python_import:
	# Running python import:
	$(PYTHON) -c "import $(TARGET_MODULE).__main__"
	# :: python import passed ::

non_final_globals:
	## Checking for non-Final globals:
	#./maintenance_scripts/get_non_final_expressions.sh $(TARGETS)
	## :: check passed ::

unreasonable_globals:
	## Checking for unreasonable global vars:
	#./maintenance_scripts/get_global_expressions.sh $(TARGETS)
	## :: check passed ::

ruff:
	# Checking Ruff rules up-to-date:
	diff --color -u \
		<(awk '/select = \[/,/]/' pyproject.toml \
			| sed -e 's|", "|/|g' \
			| head -n -1 \
			| tail -n +2 \
			| tr -d '",\#' \
			| awk '{print $$1;}' \
			| sort) \
		<($(RUFF) linter \
			| awk '{print $$1;}' \
			| sort)
	# Running ruff...
	$(RUFF) check $(TARGETS)
	# :: ruff passed ::

flake8:
	# Running flake8:
	$(PYTHON) -m flake8 $(TARGETS)
	# :: flake8 passed ::

pylint:
	# Running pylint:
	$(PYTHON) -m pylint $(TARGETS) --score no
	# :: pylint passed ::

mypy:
	# Running mypy:
	$(PYTHON) -m mypy $(TARGETS) --no-error-summary
	# :: mypy passed ::

vulture:
	# Running vulture:
	$(PYTHON) -m vulture $(TARGETS) \
		--min-confidence=1 \
		--sort-by-size
	# :: vulture passed ::

shellcheck:
	# shellcheck disable=SC2046
	## Running shellcheck:
	#( \
	#	cd $(APP_DIR) || exit ; \
	#	shellcheck $$(find . \
	#		-name '*.sh' \
	#	) \
	#)
	## :: shellcheck passed ::

shellcheck_makefile:
	## Running shellcheck on Makefile...
	#( \
	#    cd $(APP_DIR) || exit ; \
	#    $(PYTHON) ./maintenance_scripts/makefile_shellcheck.py ; \
	#)
	## :: shellcheck makefile passed ::

validate_pyproject:
	# Validate pyproject file...
	( \
		exit_code=0 ; \
		result=$$(validate-pyproject pyproject.toml 2>&1) || exit_code=$$? ; \
		if [[ $$exit_code -gt 0 ]] ; then \
			echo "$$result" ; \
			exit $$exit_code ; \
		fi \
	)
	# :: pyproject validation passed ::

lint: compile_all python_import non_final_globals unreasonable_globals ruff flake8 pylint mypy vulture shellcheck shellcheck_makefile validate_pyproject
