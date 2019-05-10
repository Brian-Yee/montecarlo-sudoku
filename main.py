#!/usr/bin/env python3
# pylint: disable=pointless-string-statement
"""
Sudoku Solver

A sudoku solver that relies on Monte Carlo techniques.
"""
import argparse
import os

from src.io import read_sudoku_file, print_sudoku
from src.indexer import Indexer

from src.backtrack import backtrack
from src.mcmc_simple import mcmc_simple


def main(sudoku_fpath, solving_method):
    """
    Main function module for Monte Carlo Sudoku Solver.

    Arguments:
        sudoku_fpath: str
            File path leading to sudoku file.
        solving_method: str
            Method for solving sudoku array.
    """
    sudoku = read_sudoku_file(sudoku_fpath)
    indexer = Indexer(sudoku)

    if solving_method == "backtrack":
        solving_func = backtrack
    elif solving_method == "mcmc_simple":
        solving_func = mcmc_simple
    else:
        raise ValueError("Unknown Method")

    try:
        sudoku = solving_func(sudoku, indexer)
    except KeyboardInterrupt:
        print("Method killed by user.")
        print("Last state observed:")
        print_sudoku(sudoku, indexer)
        exit(0)

    line = 2 * sudoku.shape[1] * "_"

    print(line)
    if sudoku is None:
        print("Unable to solve sudoku using {method}".format(method=solving_method))
        print("Last state observed:")
    else:
        print("Solved")
    print(line)

    print_sudoku(sudoku, indexer)


def parse_arguments(solving_methods):
    """
    Main CLI for interfacing with Monte Carlo Sudoku Solver.

    Arguments:
        solving_methods: tuple(str)
            Methods for solving sudoku puzzles.

    Returns:
        argparse.Namespace
            Argparse namespace containg CLI inputs.

    """
    parser = argparse.ArgumentParser(description=("Write description here"))

    parser.add_argument("sudoku_fpath", type=str, help="Sudoku file to be solved.")

    parser.add_argument(
        "solving_method",
        type=str,
        help="Methods for solving sudoku: " + ", ".join(solving_methods),
    )

    return parser.parse_args()


def assert_argument_vals(args, solving_methods):
    """
    Various asserts to enforce CLI arguments passed are valid.

    Arguments:
        args: argparse.Namespace
            Argparse namespace containing CLI inputs.
    """
    assert os.path.exists(args.sudoku_fpath) and os.path.isfile(
        args.sudoku_fpath
    ), "Invalid file passed, was it type correctly?"

    assert (
        args.solving_method in solving_methods
    ), "Invalid solving method. For full list use flag -h."


if __name__ == "__main__":
    """
    CLI for parsing and validating values passed to the Monte Carlo Sudoku Solver.
    """

    VALID_METHODS = ("backtrack", "mcmc_simple")

    ARGS = parse_arguments(VALID_METHODS)

    assert_argument_vals(ARGS, VALID_METHODS)

    main(ARGS.sudoku_fpath, ARGS.solving_method)
