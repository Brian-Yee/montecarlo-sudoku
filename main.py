#!/usr/bin/env python3
# pylint: disable=pointless-string-statement
"""
Monte Carlo Sudoku Solver

A sudoku solver that relies on Monte Carlo techniques.
"""
import argparse
import os

import numpy as np

import src.standard_sudoku


def main(sudoku_fpath, technique):
    """
    Main function module for Monte Carlo Sudoku Solver.

    Arguments:
        sudoku_fpath:
            File path leading to sudoku file.
    """
    with open(sudoku_fpath, "r") as fptr:
        sudoku = np.array([x.split() for x in fptr]).astype(np.uint8)
    src.standard_sudoku.solve(sudoku, technique)


def parse_arguments():
    """
    Main CLI for interfacing with Monte Carlo Sudoku Solver.

    Returns:
        argparse.Namespace
            Argparse namespace containg CLI inputs.

    """
    parser = argparse.ArgumentParser(description=("Write description here"))

    parser.add_argument("sudoku_fpath", type=str, help="Sudoku file to be solved.")

    parser.add_argument(
        "--technique",
        type=str,
        dest="technique",
        default="tempering",
        help="Monte carlo technique for solving a sudoku puzzle.",
    )
    return parser.parse_args()


def assert_argument_vals(args):
    """
    Various asserts to enforce CLI arguments passed are valid.

    Arguments:
        args: argparse.Namespace
            Argparse namespace containing CLI inputs.
    """
    assert os.path.exists(args.sudoku_fpath) and os.path.isfile(
        args.sudoku_fpath
    ), "Invalid file passed, was it type correctly?"

    valid_techniques = set(["tempering", "annealing"])
    assert (
        args.technique in valid_techniques
    ), "Invalid technique passed. Please pass techniques from\n\t{valid_techniques}".format(
        valid_techniques=valid_techniques
    )


if __name__ == "__main__":
    """
    CLI for parsing and validating values passed to the Monte Carlo Sudoku Solver.
    """

    ARGS = parse_arguments()

    assert_argument_vals(ARGS)

    main(ARGS.sudoku_fpath, ARGS.technique)
