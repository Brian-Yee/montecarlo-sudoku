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


def print_sudoku(sudoku):
    """
    Pretty prints a sudoku array.

    Arguments:
        sudoku: np.array
            Sudoku system with 0/-1 indicating empty/forbidden cells respectively.
    """
    legend = {x: str(x) for x in range(1, 10)}
    legend = {**legend, -1: " ", 0: "_"}
    for row in sudoku:
        print(" ".join(legend[x] for x in row))
