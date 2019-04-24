#!/usr/bin/env python3
"""
Standard recipes common to all sudoku solvers.
"""
import random
import numpy as np

from . import mcmc_util

def solve(sudoku):
    """
    Solves a sudoku system via simulated annealing.

    Given a solved sudoku has unique elements in each column, row and specified segments
    we define as a `macrostate` of length `n` it is clear to see maximum number of
    unique elements is defined as

       243 = (3*n^4 | n=3)

    We choose to maximize the number of unique elements in an array. Which in the
    standard MC language is equivalent to this problem under a sign exchange. To achieve
    this we define the energy as

        E = 243 - dE

    So that a zero-case indicates to a solution.

    Arguments:
        sudoku: np.array
            A sudoku array with zeros corresponding to free values.

    Returns (by "reference"):
        sudoku: np.array
            A sudoku array attempting to be solved.
    """
    indices = mcmc_util.define_indices(sudoku)

    mcmc_util.condition(sudoku, indices)

    energy = simulated_annealing(sudoku, indices)

    if energy == 0:
        print("Solved!")
    else:
        print("Unsolved with latent energy: {energy}".format(energy=energy))

    print(sudoku)


def simulated_annealing(sudoku, indices, sweeps=1000):
    """
    Performs simulated annealing to solve a sudoku puzzle.

    Arguments:
        sudoku: np.array
            A sudoku array with all cells filled most likely incorrectly.
        indices: list(Index)
            Essential indices for a sudoku array.
        sweeps:
            The number of sweeps in each tempearture step.

    Modifies:
        sudoku: np.array
            A sudoku array attempting to be solved.

    Returns:
        trued: bool
            Whether or not the sudoku array was found to be solved.
    """
    energy = mcmc_util.calc_energy(sudoku, indices)

    energies = []
    for temp in np.arange(0.5, 0, -0.01):
        temp_energy = 0
        completed_sweeps = 0
        for _ in range(sweeps):
            swap_pair = mcmc_util.new_swap_pair(indices)
            energy_diff = mcmc_util.swap_energy_diff(sudoku, swap_pair)

            if energy_diff <= 0 or np.exp(-energy_diff / temp) > random.random():
                energy += energy_diff
                sudoku[swap_pair] = sudoku[swap_pair][::-1]

            temp_energy += energy
            completed_sweeps += 1
            if energy == 0:
                break

        energies.append(temp_energy / completed_sweeps)
        if energy == 0:
            break

    return energy
