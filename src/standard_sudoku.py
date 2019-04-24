#!/usr/bin/env python3
"""
Standard recipes common to all sudoku solvers.
"""
import random
import numpy as np
import tqdm

from . import mcmc_util


def solve(sudoku, technique):
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
        technique: str
            Monte carlo technique to use for solving sudoku.

    Returns (by "reference"):
        sudoku: np.array
            A sudoku array attempting to be solved.
    """
    indices = mcmc_util.define_indices(sudoku)
    steps_in_sweep = sum(len(idx.free) for idx in indices)

    mcmc_util.condition(sudoku, indices)

    try:
        if technique == "annealing":
            energy = simulated_annealing(sudoku, indices, steps_in_sweep)
        elif technique == "tempering":
            energy = parallel_tempering(sudoku, indices, steps_in_sweep)
    except StopIteration as err:
        if err.value == "solved":
            energy = 0
        else:
            raise err

    if energy == 0:
        print("Solved!")
    else:
        print("Unsolved with latent energy: {energy}".format(energy=energy))

    print(sudoku)


def simulated_annealing(sudoku, indices, steps_in_sweep, num_sweeps=10):
    """
    Performs simulated annealing to solve a sudoku puzzle.

    Arguments:
        sudoku: np.array
            A sudoku array with all cells filled most likely incorrectly.
        indices: list(Index)
            Essential indices for a sudoku array.
        steps_in_sweep:
            The number of steps in a montecarlo sweep.
        num_sweeps:
            The number of sweeps to perform.

    Modifies:
        sudoku: np.array
            A sudoku array attempting to be solved.

    Returns:
        energy: int
            Final energy of system.
    """
    energy = mcmc_util.calc_energy(sudoku, indices)

    for temp in tqdm.tqdm(np.arange(0.5, 0, -0.01)):
        for _ in range(num_sweeps):
            energy = monte_carlo_sweeps(sudoku, indices, temp, energy, steps_in_sweep)

    return energy


def parallel_tempering(sudoku, indices, steps_in_sweep, num_sweeps=10):
    """
    Performs parallel tempering to solve a sudoku puzzle.

    Arguments:
        sudoku: np.array
            A sudoku array with all cells filled most likely incorrectly.
        indices: list(Index)
            Essential indices for a sudoku array.
        steps_in_sweep:
            The number of steps in a montecarlo sweep.
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

    temp_grid = np.arange(0.5, 0, -0.01)
    sudoku_instances = [sudoku.copy() for _ in temp_grid]
    print(sudoku_instances)

    return energy


def monte_carlo_sweeps(sudoku, indices, temp, energy, steps_in_sweep):
    """
    Performs one monte carlo step.

    Arguments:
        sudoku: np.array
            A sudoku array with all cells filled most likely incorrectly.
        indices: list(Index)
            Essential indices for a sudoku array.
        temp:
            Temperature parameter.
        energy: int
            Energy of system.
        steps_in_sweep:
            The number of steps in a montecarlo sweep.

    Modifies:
        sudoku: np.array
            A sudoku array attempting to be solved.

    Returns:
        energy_diff: int
            Final energy of system.
    """
    for _ in range(steps_in_sweep):
        energy_diff = monte_carlo_step(sudoku, indices, temp)
        energy += energy_diff
        if energy == 0:
            raise StopIteration("solved")

    return energy


def monte_carlo_step(sudoku, indices, temp):
    """
    Performs one monte carlo step.

    Arguments:
        sudoku: np.array
            A sudoku array with all cells filled most likely incorrectly.
        indices: list(Index)
            Essential indices for a sudoku array.
        temp:
            Temperature parameter.

    Modifies:
        sudoku: np.array
            A sudoku array attempting to be solved.

    Returns:
        energy_diff: int
            Final energy of system.
    """
    swap_pair = mcmc_util.new_swap_pair(indices)
    energy_diff = mcmc_util.swap_energy_diff(sudoku, swap_pair)

    if energy_diff <= 0 or np.exp(-energy_diff / temp) > random.random():
        sudoku[swap_pair] = sudoku[swap_pair][::-1]
        return energy_diff

    return 0
