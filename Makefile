NAME = fly_in
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
MAP = ./maps/easy/01_linear_path.txt
#MAP = ./maps/easy/02_simple_fork.txt
#MAP = ./maps/easy/03_basic_capacity.txt
#MAP = ./maps/medium/01_dead_end_trap.txt
#MAP = ./maps/medium/02_circular_loop.txt
#MAP = ./maps/medium/03_priority_puzzle.txt
#MAP = ./maps/hard/01_maze_nightmare.txt
#MAP = ./maps/hard/02_capacity_hell.txt
#MAP = ./maps/hard/03_ultimate_challenge.txt
#MAP = ./maps/challenger/01_the_impossible_dream.txt

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
	@if [ ! -f "$(PYTHON)" ]; then \
		echo "❌ Virtual environment not found."; \
		echo "Run first: make install"; \
		exit 1; \
	fi
	PYTHONPATH=. $(PYTHON) -m $(NAME) $(MAP) $(RENDER)

debug:
	PYTHONPATH=. $(PYTHON) -m pdb -m $(NAME) $(MAP)


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
# PHONY
# --------------------------

.PHONY: all venv install run debug clean clean-venv lint lint-strict