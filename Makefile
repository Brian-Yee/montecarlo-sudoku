# META ]--------------------------------------------------------------------------------------------
.PHONY: help.stub help
help.stub: help

RED="\033[91m"
END="\033[0m"

help:
	@echo "help                 Display this message."
	@echo "test                 Run testing suite."
	@echo "clean                Remove artificats of build and standardize repo."
	@echo "deps                 Install dependencies."
	@echo "sudoku.{method}      Solve an example sudoku using {method}"
	@echo "profile.{method}     Perform a cursory profile on {method}"
	@echo ""
	@echo "{methods}            Methods available for passing to a target namespace."
	@echo "    backtrack        Backtracking bruteforce algorithm."
	@echo "    mcmc_simple      Simple constant temperature MCMC."

# CORE ]--------------------------------------------------------------------------------------------
.PHONY: test clean deps

test:
	black --check .
	pylint *.py src

clean:
	black .
	-rm profile_statistics.txt

deps:
	pip install -r requirements.txt

# EXAMPLES ]----------------------------------------------------------------------------------------
.PHONY: sudoku.mcmc_simple sudoku.backtrack

sudoku.mcmc_simple:
	python main.py data/wikipedia.txt mcmc_simple

sudoku.backtrack:
	python main.py data/wikipedia.txt backtrack

# DEV ]---------------------------------------------------------------------------------------------
.PHONY: profile.mcmc_simple profile.backtrack

profile=python -m cProfile -s cumtime main.py

profile.mcmc_simple:
	$(profile) data/wikipedia.txt mcmc_simple > profile_statistics.txt
	head -30 profile_statistics.txt

profile.backtrack:
	$(profile) data/wikipedia.txt backtrack > profile_statistics.txt
	head -30 profile_statistics.txt
