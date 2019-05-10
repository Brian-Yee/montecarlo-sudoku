#!/usr/bin/env python3
"""
Function for implementing the backtracking algorithm for solving sudoku systems.
"""
from collections import deque
import numpy as np


def backtrack(sudoku, indexer):
    """
    Solve sudoku system with backtracking algorithm.

    Arguments:
        sudoku: np.array
            A sudoku puzzle, 0/-1 indicate empty and forbideen cells respectively.
        indexer: src.indexer.Indexer
            Essential indices for manipulating a Sudoku system.

    Returns:
        sudoku: np.array
            A solved sudoku puzzle.
    """
    free_coords = np.hstack(map(np.vstack, indexer.free)).T
    next_possible_state = deque((x, 0) for x in free_coords)
    proposed_states = deque()

    while next_possible_state:
        coord, idx = next_possible_state.pop()
        allowed = indexer.allowed[indexer.cell_to_block[tuple(coord.tolist())]]

        if idx == len(allowed):
            sudoku[coord[0], coord[1]] = 0
            next_possible_state.append((coord, 0))

            if proposed_states:
                coord, idx = proposed_states.pop()
                sudoku[coord[0], coord[1]] = 0
                next_possible_state.append((coord, idx + 1))
        elif any(allowed[idx] in sudoku[slices] for slices in indexer.crosses(*coord)):
            next_possible_state.append((coord, idx + 1))
        else:
            sudoku[coord[0], coord[1]] = allowed[idx]
            proposed_states.append((coord, idx))

    return sudoku
