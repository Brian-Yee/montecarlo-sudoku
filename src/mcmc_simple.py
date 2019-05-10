#!/usr/bin/env python3
"""
Simple one temperature monte carlo sudoku Solver
"""
import itertools
import random

import numpy as np


def mcmc_simple(sudoku, indexer, temp=0.3):
    """
    Solve sudoku system with backtracking algorithm.

    Arguments:
        sudoku: np.array
            A sudoku puzzle, 0/-1 indicate empty and forbideen cells respectively.
        indexer: src.indexer.Indexer
            Essential indices for manipulating a Sudoku system.
        temp:
            Temperature parameter for introducing thermal disorder. Hand tuned value of
            0.3 seems to yield good results

    Returns:
        sudoku: np.array
            A solved sudoku puzzle.
    """
    for free, allowed in zip(indexer.free, indexer.allowed):
        sudoku[free] = allowed

    energy = _energy(sudoku, indexer)

    while energy != 0:
        trial_swap = new_swap_pair(indexer.free)
        energy_diff = swap_energy_diff(sudoku, trial_swap, indexer)
        if energy_diff <= 0 or np.exp(-energy_diff / temp) > random.random():
            sudoku[trial_swap] = sudoku[trial_swap][::-1]
            energy += energy_diff

    return sudoku


def new_swap_pair(free):
    """
    Generate a pair of unique coordinates from the same macro group.

    Arguments:
        free: np.array
            xy-values of free indices grouped by their common residing blocks.

    Returns:
        coord: list(list)
            Coordinates for two unique points from the same macro group.
    """
    free_in_block = random.sample(free, 1)[0]
    free_in_block = np.vstack(free_in_block)
    pair_idx = random.sample(range(free_in_block.shape[1]), 2)
    coord = [[free_in_block[y][x] for x in pair_idx] for y in range(2)]
    return coord


def swap_energy_diff(sudoku, swap_pair, indexer):
    """
    Calculates energy difference of a proposed swap.

    Note the only change in energy can come from the lines and verticals intersecting
    the swap pair being proposed

        +---------+---------+---------+            +---------+---------+---------+
        | .  .  . | .  .  . | .  .  . |            | .  .  . | a  .  b | .  .  . |
        | .  .  . | .  .  . | .  .  . |            | .  .  . | a  .  b | .  .  . |
        | .  .  . | .  .  . | .  .  . |            | .  .  . | a  .  b | .  .  . |
        +---------+---------+---------+            +---------+---------+---------+
        | .  .  . | .  .  . | .  .  . |            | .  .  . | a  .  b | .  .  . |
        | .  .  . | A  .  . | .  .  . |     ->     | a  a  a | A  a  * | a  a  a |
        | .  .  . | .  .  B | .  .  . |            | b  b  b | *  b  B | b  b  b |
        +---------+---------+---------+            +---------+---------+---------+
        | .  .  . | .  .  . | .  .  . |            | .  .  . | a  .  b | .  .  . |
        | .  .  . | .  .  . | .  .  . |            | .  .  . | a  .  b | .  .  . |
        | .  .  . | .  .  . | .  .  . |            | .  .  . | a  .  b | .  .  . |
        +---------+---------+---------+            +---------+---------+---------+

    Here A, B are the proposed swap pair within the same block and the vertical
    lines associate with them individually are a and b respectively. A cell associated
    with both is denoted `*`. Let E_r(v, p), E_c(v, p) be functions that return unique

    Arguments:
        sudoku: np.array
            A sudoku array.
        swap_pair: list(list(int, int))
            A pair of coordinates within the same block.
        indexer: src.indexer.Indexer

    Returns:
        energy_diff: int
            Negative multiple of the number of unique numbers both col- and row-wise.
    """
    energy_slices = []
    for i in range(2):
        coord = [x[i] for x in swap_pair]
        energy_slices += indexer.crosses(*coord)

    energy_diff = 0
    for sign in [1, -1]:
        sudoku[swap_pair] = sudoku[swap_pair][::-1]
        for slices in energy_slices:
            energy_diff += sign * -np.unique(sudoku[slices]).size

    return energy_diff


def _energy(sudoku, indexer):
    """
    Calculates initial energy distribution.

    Arguments:
        sudoku: np.array
            A sudoku array with all cells filled most likely incorrectly.
        indices: list(Index)
            Essential indices for a sudoku array.

    Returns:
        energy: int
            Energy of a system with a solved case corresponding to zero.
    """
    energy = 0
    num_rows, num_cols = sudoku.shape
    for coord in itertools.product(range(num_rows), range(num_cols)):
        for slices in indexer.crosses(*coord):
            energy += 9 - len(set(sudoku[slices].flatten()))

    assert energy % 9 == 0, "Invalid calcultion."

    # normalize for double counts
    energy //= 9

    energy += sum(9 - len(set(sudoku[block].flatten())) for block in indexer.blocks)

    return energy
