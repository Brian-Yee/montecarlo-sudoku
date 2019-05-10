# A Monte Carlo Sudoku Solver
Algorithms for solving Sudoku puzzles.

# Implementations
Current implementations include:
  - Backtracking
  - Simple Markov Chain Monte Carlo

# Input Format
Sudokus are written as seen with `0`s denoting empty cells. For example the example sudoku given on the Wikipedia article is written as.

```
5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9
```

# Use
Preset examples are given in the makefile

```
> make
help                       Display this message.
test                       Run testing suite.
clean                      Remove artificats of build and standardize repo.
deps                       Install dependencies.
sudoku.{method}            Solve an example sudoku using {method}.
double-{joint}.{method}    Solve a double sudoku {joint}-block joined sytem using method.
profile.{method}           Perform a cursory profile on {method}

Vars
{methods}                  Methods available for passing to a target namespace.
    backtrack                  Backtracking bruteforce algorithm.
    mcmc_simple                Simple constant temperature MCMC.
{joint}                    Side length of conjoined blocks in generalized sudoku systems.
    1, 2                       Integer values always less than blockwidth of a sudoku.
```

Interface info for the main module is accessible via flag `-h`

```
> python main.py -h
usage: main.py [-h] sudoku_fpath solving_method

Write description here

positional arguments:
  sudoku_fpath    Sudoku file to be solved.
  solving_method  Methods for solving sudoku: backtrack, mcmc_simple

optional arguments:
  -h, --help      show this help message and exit
```
