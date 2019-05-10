# An MCMC Python Generalized Sudoku System Solver

Algorithms for solving generalized Sudoku (standard, twin, triple, samurai, etc..) puzzles.

Current implementations include:
  - Backtracking
  - Simple Markov Chain Monte Carlo
  
**Further implementations/generalization notes are written at the bottom.***

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

# How to Contribute

Feel free to submit a PR! If any of the below optimizations/generalizations not being implemented
below rustle your jimmies feel free to fork and submit a PR.

## (Easy) Add Method Timeouts

Currently algorithms just keep going. Use `subprocess` to terminate a method if it exceeds a user
specified time.

## (Easy) Hexadoku Support (Really n-doku)

Sudoku is composed of 3x3 blocks arranged in a 3x3 grid filled with numbers 1 to 3^2. Hexadoku is
the same except instead of using 3 for everything 4 is used for everything. A lot of the code was
writing in a general fashion to support hexadoku or `n`-doku's in general. A great additional 
feature would be instantly identifying and solving any `n`-doku passed under the same file format.

## (Easy) MCMC Statistics tracking

Track and create the ability to visualize statistical quantities. Something like energy histograms
or curves would be neat to see if any phase transition-like behaviour can be observed.

## (Hard) Parallel Tempering

It would be ideal to not have to tune the temperature parameter. This can be achieved through 
 [parallel tempering](https://en.wikipedia.org/wiki/Parallel_tempering)
tempering to run multiple copies which can then perform macro-state swaps between energies of
different systems. The actual mechanics of this method is near trivial with the complexity arising out
of the temperature domain grid being used requiring an optimal spacing.

## (Hard) Constraint Propagation

While writing this program I came across the following
 [article](http://www.norvig.com/sudoku.html)
by
 [Peter Norvig](https://en.wikipedia.org/wiki/Peter_Norvig)
implement his method to solve sudoku systems as defined in this program. It would be wonderful to
have the ground truth accessible to see where and how MCMC fails. Also as I am not an expert in
constraint propagation it would be neat to see how it scales in generalized systems.

