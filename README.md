# An MCMC Python Generalized Sudoku System Solver

Algorithms for solving generalized Sudoku (standard, twin, triple, samurai, etc..) puzzles.

Current implementations include:
  - Backtracking
  - Simple Markov Chain Monte Carlo

Results have been demonstrated to work on various generalized (and normal) sudoku puzzles but
obviously your mileage may vary depending on the difficulty of the sudoku puzzle presented. This
repository was more of a relaxing exercise in creating a MCMC program and more efficient and
robust methods can be found elsewhere. However, it is a fun problem to demonstrate the versatility
of Monte Carlo Methods.

## Example

Below is a Samurai Sudoku published by the Washington Post on 2018-10-14. The temperature
parameter of the simple MCMC was quickly tuned by hand to `0.25` which corresponded to finding a
solution in `74.66s`. Simple backtracking tested for up to `3` minutes (because aint no body got
time for that) fails to identify the solution illustrating the use of stochastic state space search
over exhaustive methods.

```
. 7 . 8 . 9 . 4 .       . 1 . 6 . 7 . 8 .        3 7 1 8 2 9 6 4 5       5 1 3 6 4 7 2 8 9
. . . 6 . 1 . . .       . . . 2 . 9 . . .        4 5 9 6 7 1 8 3 2       6 7 4 2 8 9 3 1 5
. . 8 . 4 . 1 . .       . . 2 . 5 . 4 . .        6 2 8 3 4 5 1 7 9       9 8 2 3 5 1 4 6 7
7 8 . . . . . 6 3       2 3 . . . . . 7 6        7 8 2 9 1 4 5 6 3       2 3 5 1 9 4 8 7 6
1 . . 5 8 7 . . 4       7 . . 5 6 8 . . 3        1 3 6 5 8 7 2 9 4       7 4 1 5 6 8 9 2 3
5 9 . . . . . 1 8       8 9 . . . . . 5 4        5 9 4 2 3 6 7 1 8       8 9 6 7 2 3 1 5 4
. . 5 . 6 . . . . 2 . 5 . . . . 3 . 7 . .        9 4 5 1 6 2 3 8 7 2 4 5 1 6 9 8 3 5 7 4 2
. . . 7 . 8 . . . 8 . 9 . . . 4 . 6 . . .        2 1 3 7 9 8 4 5 6 8 1 9 3 2 7 4 1 6 5 9 8
. 6 . 4 . 3 . . . . 6 . . . . 9 . 2 . 3 .        8 6 7 4 5 3 9 2 1 3 6 7 4 5 8 9 7 2 6 3 1
            5 7 . . . . . 1 4                                5 7 3 9 2 6 8 1 4
            1 . . 7 5 8 . . 2                                1 4 9 7 5 8 6 3 2
            2 6 . . . . . 7 5                                2 6 8 4 3 1 9 7 5
. 5 . 1 . 3 . . . . 7 . . . . 1 . 6 . 2 .        7 5 8 1 2 3 6 9 4 1 7 2 5 8 3 1 4 6 7 2 9
. . . 4 . 8 . . . 6 . 4 . . . 3 . 7 . . .        9 2 1 4 6 8 7 3 5 6 8 4 2 9 1 3 5 7 4 6 8
. . 6 . 7 . . . . 5 . 3 . . . . 2 . 1 . .        3 4 6 5 7 9 8 1 2 5 9 3 7 4 6 8 2 9 1 3 5
1 6 . . . . . 4 9       3 5 . . . . . 9 4        1 6 3 7 8 2 5 4 9       3 5 8 7 6 1 2 9 4
2 . . 3 9 4 . . 8       1 . . 5 3 4 . . 7        2 7 5 3 9 4 1 6 8       1 2 9 5 3 4 6 8 7
4 8 . . . . . 7 3       4 6 . . . . . 5 1        4 8 9 6 5 1 2 7 3       4 6 7 9 8 2 3 5 1
. . 4 . 3 . 9 . .       . . 4 . 9 . 8 . .        5 1 4 8 3 6 9 2 7       6 1 4 2 9 5 8 7 3
. . . 2 . 5 . . .       . . . 6 . 3 . . .        6 9 7 2 4 5 3 8 1       8 7 5 6 1 3 9 4 2
. 3 . 9 . 7 . 5 .       . 3 . 4 . 8 . 1 .        8 3 2 9 1 7 4 5 6       9 3 2 4 7 8 5 1 6
```

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

Forbidden cells for generalized systems are denoted with a `.` for increased legibility. As an
example a 2-sudoku conjoined by 1 block is written below as

```
1 0 5 8 2 0 0 6 7 . . . . . .
6 0 0 0 0 4 0 9 0 . . . . . .
0 0 4 7 0 0 3 0 8 . . . . . .
0 9 8 2 5 0 0 0 0 . . . . . .
3 0 0 4 6 0 2 0 0 . . . . . .
7 6 0 0 8 3 0 1 0 . . . . . .
2 0 0 1 0 0 0 7 0 1 0 0 0 6 9
0 7 9 0 0 0 6 2 0 0 0 0 7 0 4
8 0 3 0 0 0 0 0 5 6 8 0 3 2 0
. . . . . . 3 0 0 0 6 4 0 0 8
. . . . . . 0 1 0 9 0 0 0 5 0
. . . . . . 4 0 9 0 0 0 0 7 3
. . . . . . 0 0 4 0 7 9 2 0 0
. . . . . . 0 0 8 0 5 0 0 1 0
. . . . . . 5 9 7 2 0 3 0 0 0
```

# Usage
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

# TODO

It would be ideal to not have to tune the temperature parameter. This can be achieved through parallel
tempering to run multiple copies. As such, this is the next natural step for the project, if you're
interested feel free to submit a PR!
