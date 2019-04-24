#!/usr/bin/env python3
"""
Common utility functions required for solving Monte Carlo recipes.
"""
import random
import numpy as np

from dataclasses import dataclass  # back port of python3.7 class


@dataclass  # pylint: disable=too-few-public-methods
class Index:
    """
    Groups essential indices for manipulating a subsection of a Sudoku array.

    macros: np.array
        Macrostates (quadrants) of a sudoku array ordered left-right, top-down.
    free: list(tuple(tuple, tuple))
        Cells free to be mutated.
    pinned: list(tuple(tuple, tuple))
        Cells which were defined at instantiation and thus immutable.
    """

    macro: tuple
    free: tuple
    pinned: tuple


def define_indices(sudoku):
    """
    Derives essential indices fro accessing sudoku array by reference.

    Indices of each return argument are aligned
    Arguments:
        sudoku: np.array
            A sudoku array with zeros corresponding to free values.

    Returns:
        list(Index)
            Essential indices for a sudoku array.
    """
    macros = np.array([[3 * (x // 3) + y // 3 for y in range(9)] for x in range(9)])
    macros = [np.where(macros == x) for x in range(9)]

    free, pinned = [], []
    is_free = sudoku == 0
    for macro in macros:
        in_macro = np.full_like(sudoku, False)
        in_macro[macro] = True
        free.append(np.where(is_free & in_macro))
        pinned.append(np.where(~is_free & in_macro))

    return [Index(a, b, c) for a, b, c in zip(macros, free, pinned)]


def calc_energy(sudoku, indices):
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
    energy = 3 * sudoku.shape[0] ** 2

    for index in indices:
        energy -= len(set(sudoku[index.macro].flatten()))

    energy -= sum(len(set(sudoku[x, :])) for x in range(sudoku.shape[0]))
    energy -= sum(len(set(sudoku[:, x])) for x in range(sudoku.shape[1]))

    return energy


def new_swap_pair(indices):
    """
    Generate a pair of unique coordinates from the same macro group.

    Arguments:
        indices: list(Index)
            Essential indices for a sudoku array.

    Returns:
        coord: list(list)
            Coordinates for two unique points from the same macro group.
    """
    index = indices[random.randint(0, 8)]
    pair_idx = random.sample(range(len(index.free[0])), 2)
    coord = [[index.free[y][x] for x in pair_idx] for y in range(2)]
    return coord


def swap_energy_diff(sudoku, swap_pair):
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
        | .  .  . | A  .  . | .  .  . |     ->     | a  a  a | A  a  # | .  .  . |
        | .  .  . | .  .  B | .  .  . |            | b  b  b | *  b  B | b  b  b |
        +---------+---------+---------+            +---------+---------+---------+
        | .  .  . | .  .  . | .  .  . |            | .  .  . | a  .  b | .  .  . |
        | .  .  . | .  .  . | .  .  . |            | .  .  . | a  .  b | .  .  . |
        | .  .  . | .  .  . | .  .  . |            | .  .  . | a  .  b | .  .  . |
        +---------+---------+---------+            +---------+---------+---------+

    Here A, B are the proposed swap pair within the same macro unit and the vertical
    lines associate with them individually are a and b respectively. A cell associated
    with both is denoted `*`. Let E_r(v, p), E_c(v, p) be functions that return unique
    elements along the row and columns respectively if a value `v` is inserted at point
    `p`. Thus the change in swap energy is defined as:

        | dE | = | E_r(B, A) + E_r(A, B) - E_r(A, A) + E_r(B, B) |

    We choose to maximize the number of unique elements in an array. Which in the
    standard MC language is equivalent to this problem under a sign exchange. To achieve
    this we define the energy as

        dE = - ( E_r(A, A) + E_r(B, B) -  E_r(B, A) + E_r(A, B) )

    Arguments:
        sudoku: np.array
            A sudoku array.

    Returns:
        energy_diff: int
            Negative multiple of the number of unique numbers both col- and row-wise.
    """
    sudoku[swap_pair] = sudoku[swap_pair][::-1]

    # fmt: off
    energy_diff = (
        -sum(len(set(sudoku[x, :])) for x in swap_pair[0])
        -sum(len(set(sudoku[:, x])) for x in swap_pair[1])
    )
    # fmt: on

    sudoku[swap_pair] = sudoku[swap_pair][::-1]

    # fmt: off
    energy_diff -= (
        -sum(len(set(sudoku[x, :])) for x in swap_pair[0])
        -sum(len(set(sudoku[:, x])) for x in swap_pair[1])
    )
    # fmt: on

    return energy_diff


def condition(sudoku, indices):
    """
    Conditions distributino on obeying the rule of complete sets for each segment.

    Arguments:
        sudoku: np.array
            A sudoku array with zeros corresponding to free values.
        indices: list(Index)
            Essential indices for a sudoku array.

    Modifies:
        sudoku: np.array
            A sudoku array with all cells filled most likely incorrectly.
    """
    for index in indices:
        immutable_values = set(sudoku[index.pinned])
        mutable_values = [x for x in range(1, 10) if x not in immutable_values]
        sudoku[index.free] = random.sample(mutable_values, len(mutable_values))
