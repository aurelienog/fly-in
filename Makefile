NAME = fly_in
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

# --------------------------
# DEFAULT
# --------------------------

all: install

# --------------------------
# VENV
# --------------------------

venv:
	python3 -m venv $(VENV)

# --------------------------
# INSTALL
# --------------------------

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# --------------------------
# RUN
# --------------------------

run:
	PYTHONPATH=. $(PYTHON) -m $(NAME) config.txt

debug:
	PYTHONPATH=. $(PYTHON) -m pdb -m $(NAME) config.txt


# --------------------------
# CLEAN
# --------------------------

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

clean-venv: clean
	rm -rf $(VENV)

# --------------------------
# LINT
# --------------------------

lint:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --strict

# --------------------------
# BUILD
# --------------------------

build: install
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build

# --------------------------
# PHONY
# --------------------------

.PHONY: all venv install run debug clean clean-venv lint lint-strict build