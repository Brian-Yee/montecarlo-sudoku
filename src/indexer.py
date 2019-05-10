#!/usr/bin/env python3
"""
Preprocessing functions for identifying useful bookkeeping data structures.

Coordinates denotes cartesian position while indices refers to indexing structures. In
numpy these are transposed by definition. A list of coordinate _points_ is given as:

    [(x1, y1), ..., (x_n, y_n)]

while the _indices_ are given by

    [(x1, ..., x_n), (y1,...,y_n)]
"""
import itertools
import numpy as np


class Indexer:
    """
    Essential indices for manipulating a Sudoku system.

    Subsudokus are indexed subrow-wise in order of appearance row-wise.
    For example a diagonal 3-system sudoku with 2x2 squares interlocked along the
    diagonal produces the following block ordering as each subsudoku is identified:

         0  1  2   .   .      0  1  2   .   .      0  1  2   .   .
         3  4  5   .   .      3  4  5   9   .      3  4  5   9   .
         6  7  8   .   .  ->  6  7  8  10   .  ->  6  7  8  10  14
         .  .  .   .   .      . 11 12  13   .      . 11 12  13  15
         .  .  .   .   .      .  .  .   .   .      .  . 16  17  18
    """

    def __init__(self, sudoku):
        """
        Defines a sudoku in terms of a system with parameters to be solved.

        Arguments:
            sudoku:
                A sudoku puzzle, 0/-1 indicate empty and forbideen cells respectively.
        """
        self._crosses, self._blocks = _energy_crosses_and_blocks(sudoku)
        self._cell_to_block = _cell_to_block(self._blocks, *sudoku.shape)

        self._free, self._pinned = _neighbours(sudoku, self._blocks)
        self._allowed = [
            [y for y in range(1, 10) if y not in sudoku[pinned]]
            for pinned in self._pinned
        ]

    @property
    def allowed(self):
        """
        Initially allowed cell values indexed by block.

        Returns:
            _allowed: list(list(int))
                Allowed cell values.
        """
        return self._allowed

    @property
    def free(self):
        """
        Indices of cell positions free to be mutated within a given block.

        Returns:
            _free: list(tuple(np.array, np.array))
                Indices free to be mutated.
        """
        return self._free

    @property
    def blocks(self):
        """
        Indices of cell positions within each block.

        Returns:
            _free: list(tuple(np.array, np.array))
                Cell positions of each block.
        """
        return self._blocks

    @property
    def cell_to_block(self):
        """
        Maps a coordinate cell to a corresponding block index.

        For example:
           . . . . . . . . .
           . a . . b . . . .
           . . . . . . . c .
           . . . . . . . . .
           . . . d . . . . .
           . . . . . . . . .
           . . . . . . . . .
           . . . e . . . . .
           . . . . . f . . .

        Coordinates (a, b, c, d, e, f),  map to block indices (0, 1, 2, 4, 7, 7)

        Returns:
            _cell_to_block: dict(tuple(int, int), int)
                Hashmapping of cell coordinate to block coordinate
        """
        return self._cell_to_block

    def crosses(self, *cell):
        """
        Returns energy crossings for a given cell.

        Arguments:
            cell: tuple(int, int)
                A sudoku system cell given in x-y coordinates.

        Returns:
            list(tuple(slice, slice))
        """
        return self._crosses[cell[0]][cell[1]]


def _energy_crosses_and_blocks(sudoku):
    """
    Define energy crosses for every cell.

    Energy crosses are defined as the rows and cells of an individual sudoku that
    intersect with a given cell. Note due to the interlocking nature of generalized
    sudoku puzzles multiple energy crosses can exist for a given square. For example,
    consider a point `o` and the corresponding energy cross defined by `x`
        _ _ _ _ _ x _ _ _
        _ _ _ _ _ x _ _ _
        _ _ _ _ _ x _ _ _
        x x x x x o x x x
        _ _ _ _ _ x _ _ _
        _ _ _ _ _ x _ _ _
        _ _ _ _ _ x _ _ _
        _ _ _ _ _ x _ _ _
        _ _ _ _ _ x _ _ _

    Arguments:
        sudoku: np.array
            A sudoku puzzle, 0/-1 indicate empty and forbideen cells respectively.

    Returns:
        crosses: tuple(list(tuple(slice, slice)))
            Grid of potentially multi-length lists containing slicing indices defining
            the energy crosses which intersect the respective grid cells.
        blocks: tuple(tuple(np.array, np.array))
            Blocks of a sudoku array.
    """
    num_rows, num_cols = sudoku.shape
    crosses = [[tuple([]) for _ in range(num_cols)] for _ in range(num_rows)]

    blocks = np.full_like(sudoku, -1)
    counter = 0
    for row, col in itertools.product(range(num_rows - 8), range(num_cols - 8)):
        if (sudoku[row : row + 9, col : col + 9] == -1).any():
            continue

        for subrow, subcol in itertools.product(range(0, 9, 3), range(0, 9, 3)):
            if blocks[row + subrow, col + subcol] != -1:
                continue
            blocks[
                row + subrow : row + subrow + 3, col + subcol : col + subcol + 3
            ] = counter
            counter += 1

        for subrow, subcol in itertools.product(range(9), range(9)):
            i, j = row + subrow, col + subcol
            crosses[i][j] += (
                (slice(i - subrow, i + 9 - subrow), slice(j, j + 1)),
                (slice(i, i + 1), slice(j - subcol, j + 9 - subcol)),
            )

    blocks = [np.where(blocks == x) for x in range(blocks.max() + 1)]
    blocks = [x for x in blocks if not np.any(sudoku[x] == -1)]

    return map(tuple, (crosses, blocks))


def _neighbours(sudoku, blocks):
    """
    Defines neighbours within the same block.

    For example consider the point `o` and corresponding neighbours `x`
        _ _ _ _ _ _ _ _ _
        _ _ _ _ _ _ _ _ _
        _ _ _ _ _ _ _ _ _
        _ _ _ _ _ _ x x x
        _ _ _ _ _ _ x x o
        _ _ _ _ _ _ x x x
        _ _ _ _ _ _ _ _ _
        _ _ _ _ _ _ _ _ _
        _ _ _ _ _ _ _ _ _

    Arguments:
        sudoku: np.array
            A sudoku puzzle, 0/-1 indicate empty and forbideen cells respectively.

    Returns:
        free: tuple(tuple(np.array, np.array))
            Cells within block free to be mutated.
        pinned: tuple(tuple(np.array, np.array))
            Cells within block which were defined at instantiation and thus immutable.
    """
    free, pinned = [], []
    is_free = sudoku == 0
    for block in blocks:
        in_block = np.full_like(sudoku, False)
        in_block[block] = True
        free.append(np.where(is_free & in_block))
        pinned.append(np.where(~is_free & in_block))

    return map(tuple, (free, pinned))


def _cell_to_block(blocks, num_rows, num_cols):
    """
    Derive Blocks from cell value passed.

    Arguments:
        blocks: tuple(tuple(np.array, np.array))
            Blocks of a sudoku array.

    Returns:
        cell_to_block: dict(tuple(int, int), int)
            Hashmapping of cell coordinate to block coordinate
    """
    cell_to_block = dict()
    for cell in itertools.product(range(num_rows), range(num_cols)):
        for idx, block_indices in enumerate(blocks):
            if cell in zip(*block_indices):
                cell_to_block[cell] = idx
                break
    return cell_to_block
