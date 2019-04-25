# META ]--------------------------------------------------------------------------------------------
.PHONY: help.stub help
help.stub: help

RED="\033[91m"
END="\033[0m"

help:
	@echo "help         Display this message."
	@echo "anneal       Solve sudoku with simulated annealing."
	@echo "temper       Solve sudoku with parallel tempering."
	@echo "test         Run testing suite."
	@echo "clean        Remove artificats of build and standardize repo."

# EXAMPLES ]----------------------------------------------------------------------------------------
.PHONY: anneal
sudoku:
	python main.py data/sudoku/test.txt

samurai:
	python main.py data/sudoku/samurai-sudoku.txt

# CORE ]--------------------------------------------------------------------------------------------
.PHONY: test clean deps

test:
	pylint *.py

clean:
	black .

deps:
	pip install -r requirements.txt
