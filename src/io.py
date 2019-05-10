#!/usr/bin/env python3
"""
Interface for custom sudoku file formats.
"""
import numpy as np


def read_sudoku_file(fpath):
    """
    Reads in a sudoku file with specified format outlined in README.

    Arguments:
        fpath: str
            File path to sudoku file.

    Returns:
        sudoku: np.array
            Sudoku system with 0/-1 indicating empty/forbidden cells respectively.
    """
    with open(fpath, "r") as fptr:
        string = fptr.read()
        if string.endswith("\n"):
            string = string[:-1]

    system = np.array([list(x[::2]) for x in string.split("\n")])
    sudoku = np.full_like(system, -1, dtype=np.int)

    for i in range(10):
        sudoku[system == str(i)] = i

    return sudoku


def print_sudoku(sudoku, indexer):
    """
    Pretty prints a sudoku array.

    Cells with violations have an `*` appended to them.

    Arguments:
        sudoku: np.array
            Sudoku system with 0/-1 indicating empty/forbidden cells respectively.
        indexer: src.indexer.Indexer
            Essential indices for manipulating a Sudoku system.
    """
    legend = {x: str(x) for x in range(1, 10)}
    legend = {**legend, -1: " ", 0: "_"}

    for i, row in enumerate(sudoku):
        for j, val in enumerate(row):
            print(legend[val], end="")
            invalid = False
            for slices in indexer.crosses(i, j):
                if np.unique(sudoku[slices].squeeze()).shape[0] != 9:
                    invalid = True
                    break
            if invalid:
                print("*", end="")
            else:
                print(" ", end="")
        print()
