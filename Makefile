# Detect OS for venv differences
OS=$(shell uname -s)

ifeq ($(OS),Linux)
    VENV=.venv/bin
else ifeq ($(OS),Darwin)
    VENV=.venv/bin
else
    VENV=.venv/Scripts
endif

# Do the normal QA, similar to the GH action
all: requirements lint test

# Lint using ruff. Will not break build
lint:
	-${VENV}/ruff -- --format=github --target-version=py310 .

# Run pytests with proper output
test:
	${VENV}/pytest -v -s 

# Run hellsnake :D
run: requirements
	${VENV}/python hell_snake.py

# Use make init to initialize venv
init: requirements
.venv:
	python -m venv .venv

# Install/Update requirements
.PHONY: requirements
requirements: .venv
	${VENV}/pip install -r requirements.txt

# Clean the venv
clean:
	ifeq ($(OS),Linux)
		rm -rf .venv
	else ifeq ($(OS),Darwin)
		rm -rf .venv
	else
		rm -r .venv
	endif

