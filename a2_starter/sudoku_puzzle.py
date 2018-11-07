-# Assignment 2 - Puzzle Game
#
# CSC148 Summer 2017, University of Toronto
# ---------------------------------------------
"""Sudoku puzzle module.

Here are the rules of Sudoku:

- The puzzle consists of an n-by-n grid, where n = 4, 9, 16, or 25.
  Each square contains a uppercase letter between A and the n-th letter
  of the alphabet, or is empty.
  For example, on a 4-by-4 Sudoku board, the available letters are
  A, B, C, or D. On a 25-by-25 board, every letter A-Y is available.
- The goal is to fill in all empty squares with available letters so that
  the board has the following property:
    - no two squares in the same row have the same letter
    - no two squares in the same column have the same letter
    - no two squares in the same *subsquare* has the same letter
  A *subsquare* is found by dividing the board evenly into sqrt(n)-by-sqrt(n)
  pieces. For example, a 4-by-4 board would have 4 subsquares: top left,
  top right, bottom left, bottom right.

Note that most, but not all, of the code is given to you already.
"""
from puzzle import Puzzle
from math import sqrt

CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class SudokuPuzzle(Puzzle):
    """Implementation of a Sudoku puzzle."""
    # === Private Attributes ===
    # @type _n: int
    #     The size of the board. Must be 4, 9, 16, or 25.
    # @type _grid: list[list[str]]
    #     A representation of the Sudoku grid. Consists of a list of lists,
    #     where each inner list represents a row of the grid.
    #
    #     Each item of the inner list is either an uppercase letter,
    #     or is the empty string '', representing an empty square.
    #     Each letter must be between 'A' and the n-th letter of the alphabet.

    def __init__(self, grid):
        """Create a new Sudoku puzzle with an initial grid 'grid'.

        Precondition: <grid> is a valid Sudoku grid.

        @type self: SudokuPuzzle
        @type grid: list[list[str]]
        @rtype: None
        """
        self._n = len(grid)
        self._grid = grid

    def __str__(self):
        """Return a human-readable string representation of <self>.

        Note that the numbers at the top and left cycle 0-9,
        to help the user when they want to enter a move.

        @type self: SudokuPuzzle
        @rtype: str

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
        ['', 'D', '', ''], ['', '', '', '']])
        >>> print(s)
          01|23
         ------
        0|AB|CD
        1|DC|BA
         ------
        2| D|
        3|  |
        <BLANKLINE>
        """
        m = int(sqrt(self._n))
        s = ''
        # Column label
        s += '  '
        for col in range(self._n):
            s += str(col % 10)
            # Vertical divider
            if (col + 1) % m == 0 and col + 1 != self._n:
                s += '|'
        # Horizontal divider
        s += '\n ' + ('-' * (self._n + m)) + '\n'
        for i in range(self._n):
            # Row label
            s += str(i % 10) + '|'
            for j in range(self._n):
                cell = self._grid[i][j]
                if cell == '':
                    s += ' '
                else:
                    s += str(cell)
                # Vertical divider
                if (j + 1) % m == 0 and j + 1 != self._n:
                    s += '|'
            s = s.rstrip()
            s += '\n'

            # Horizontal divider
            if (i + 1) % m == 0 and i + 1 != self._n:
                s += ' ' + ('-' * (self._n + m)) + '\n'

        return s

    def is_solved(self):
        """Return whether <self> is solved.

        A Sudoku puzzle is solved if its state matches the criteria
        listed at the end of the puzzle description.

        @type self: SudokuPuzzle
        @rtype: bool

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', 'D', 'C'], \
                              ['D', 'C', 'B', 'A']])
        >>> s.is_solved()
        True
        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'D', 'A', 'C'], \
                              ['D', 'C', 'B', 'A']])
        >>> s.is_solved()
        False
        """
        # Check for empty cells
        for row in self._grid:
            if '' in row:
                return False

        # Check rows
        for row in self._grid:
            if sorted(row) != list(CHARS[:self._n]):
                return False

        # Check cols
        for i in range(self._n):
            # Note the use of a list comprehension here.
            if sorted([row[i] for row in self._grid]) != list(CHARS[:self._n]):
                return False

        # Check all subsquares
        m = int(sqrt(self._n))
        for x in range(0, self._n, m):
            for y in range(0, self._n, m):
                items = [self._grid[x + i][y + j]
                         for i in range(m)
                         for j in range(m)]

                if sorted(items) != list(CHARS[:self._n]):
                    return False

        # All checks passed
        return True

    def extensions(self):
        """Return list of extensions of <self>.

        This method picks the first empty cell (looking top-down,
        left-to-right) and returns a list of the new puzzle states
        obtained by filling in the empty cell with one of the
        available letters that does not violate any of the constraints
        listed in the problem description. (E.g., if there is
        already an 'A' in the row with the empty cell, this method should
        not try to fill in the cell with an 'A'.)

        If there are no empty cells, returns an empty list.

        @type self: SudokuPuzzle
        @rtype: list[SudokuPuzzle]

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> lst = list(s.extensions())
        >>> len(lst)
        1
        >>> print(lst[0])
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA|D
        3|DC|
        <BLANKLINE>
        """
        # Search for the first empty cell
        row_index, col_index = None, None
        for i in range(self._n):
            row = self._grid[i]
            if '' in row:
                row_index, col_index = i, row.index('')
                break

        if row_index is None:
            return []
        else:
            # Calculate possible letter to fill the empty cell
            letters = self._possible_letters(row_index, col_index)
            return [self._extend(letter, row_index, col_index)
                    for letter in letters]

    def move(self, move):
        """Return a new puzzle state specified by making the given move.

        Raise a ValueError if <move> represents an invalid move.
        Do not change the state of <self>. This is not a mutating method!

        @type self: SudokuPuzzle
        @type move: str
        @rtype: SudokuPuzzle

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> print(s.move('(2,2)->D'))
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA|D
        3|DC|
        <BLANKLINE>
        >>> try:
        ...   s.move('xxxx')
        ... except Exception as e:
        ...   print(e)
        Incorrect input format!
        >>> try:
        ...   s.move('(a,a)->B')
        ... except Exception as e:
        ...   print(e)
        Index failed to be converted to integer!
        >>> try:
        ...   s.move('(-1,1)->B')
        ... except Exception as e:
        ...   print(e)
        Index out of range!
        >>> try:
        ...   s.move('(2,2)->A')
        ... except Exception as e:
        ...   print(e)
        Repetitive letter found!
        >>> try:
        ...   s.move('(1,1)->A')
        ... except Exception as e:
        ...   print(e)
        Non-empty cell found!
        >>> try:
        ...   s.move('(3,3)->1')
        ... except Exception as e:
        ...   print(e)
        Unrecognized letter!
        """
        # split the move string to the parts according to the arrow
        parts = move.split('->')
        # if the length of parts is not 2
        if len(parts) != 2:
            # raise the value error
            raise ValueError('Incorrect input format!')
        # get the first element in string
        row_col = parts[0].strip()
        # if the first and final string item is not the matched brackets
        if row_col[0] != '(' or row_col[-1] != ')':
            # raise the value error
            raise ValueError('Incorrect input format!')
        # split the string of row column by ","
        row_col = row_col[1:-1].split(',')
        # if the length of row column list is not 2
        if len(row_col) != 2:
            # raise the value error
            raise ValueError('Incorrect input format!')
        # try the following
        try:
            # get the row index and column index
            row_index, col_index = list(map(int, row_col))
        # else the value error
        except ValueError:
            # raise value error
            raise ValueError('Index failed to be converted to integer!')
        # if the row index or the column index is not in the range of grid
        if not (-1 < row_index < self._n) or not (-1 < col_index < self._n):
            # raise the value error
            raise ValueError('Index out of range!')
        # get the letter by th row and column index in the move string
        letter = parts[1].strip()
        # if the letter is not in the alphabet
        if letter not in CHARS:
            # raise the value error
            raise ValueError('Unrecognized letter!')
        # if the cell is not empty string by the row index and column index
        if self._grid[row_index][col_index] != '':
            # raise the value error
            raise ValueError('Non-empty cell found!')
        # if the letter in the each row with the matched column index
        if letter in set(self._grid[x][col_index] for x in range(self._n)):
            # raise the value error
            raise ValueError('Repetitive letter found!')
        # if the letter in the each row with the matched column index
        if letter in set(self._grid[row_index][y] for y in range(self._n)):
            raise ValueError('Repetitive letter found!')
        # get the subsquare with the length of grid
        m = int(sqrt(self._n))
        # get the base of x
        base_x = row_index // m * m
        # get the base of y
        base_y = col_index // m * m
        # check the whether there exists repetitive letter
        if letter in set(self._grid[base_x + dx][base_y + dy]
                         for dx in range(m) for dy in range(m)):
            raise ValueError('Repetitive letter found!')
        # return the obtained puzzle after the given moves
        return self._extend(letter, row_index, col_index)

    def compare(self, state):
        """Return a move obtained by comparing with <state>
        or None if no differences found

        Precondition: <state> should be one move advanced.

        @type self: SudokuPuzzle
        @type state: SudokuPuzzle
        @rtype: str | None

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> s1 = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', 'D', ''], \
                              ['D', 'C', '', '']])
        >>> s.compare(s1)
        '(2, 2) -> D'
        """
        # loop the row index in the grid
        for row in range(self._n):
            # loop the column index in the grid
            for col in range(self._n):
                # if the item in the position is not eqaul to the
                # current item in the postion of current state
                if self._grid[row][col] != state._grid[row][col]:
                    return '({}, {}) -> {}'.format(
                        row, col, state._grid[row][col])

    # ------------------------------------------------------------------------
    # Helpers for method 'extensions'
    # ------------------------------------------------------------------------
    def _possible_letters(self, row_index, col_index):
        """Return a list of the possible letters for a cell.

        The returned letters must be a subset of the available letters.
        The returned list should be sorted in alphabetical order.

        @type self: SudokuPuzzle
        @type row_index: int
        @type col_index: int
        @rtype: list[str]

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> s._possible_letters(2,2)
        ['D']
        >>> s._possible_letters(3,2)
        ['B']
        >>> s._possible_letters(2,3)
        ['C']
        >>> s._possible_letters(3,3)
        ['A']
        """
        # TODO: Change this method to only return valid moves.

        # create a set including the characters based on the board
        result = set(CHARS[:self._n])
        # loop the board, and find the letter in the each row with matched
        # column index
        result -= set(self._grid[x][col_index] for x in range(0, self._n))
        # loop the board, and find the letter in the each column with matched
        # row index
        result -= set(self._grid[row_index][y] for y in range(0, self._n))
        # get the subsquare with the length of grid
        m = int(sqrt(self._n))
        # get the base x
        base_x = row_index // m * m
        # get the base y
        base_y = col_index // m * m
        # get the all possible letters which are the subset of the available
        # letters
        result -= set(self._grid[base_x + dx][base_y + dy]
                      for dx in range(m) for dy in range(m))
        # sort the list of result and return
        return sorted(list(result))

    def _extend(self, letter, row_index, col_index):
        """Return a new Sudoku puzzle obtained after one move.

        The new puzzle is identical to <self>, except that it has
        the value at position (row_index, col_index) equal to 'letter'
        instead of empty.

        'letter' must be an available letter.
        'row_index' and 'col_index' are between 0-3.

        @type self: SudokuPuzzle
        @type letter: str
        @type row_index: int
        @type col_index: int
        @rtype: SudokuPuzzle

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> print(s._extend('B', 2, 3))
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA| B
        3|DC|
        <BLANKLINE>
        """
        new_grid = [row.copy() for row in self._grid]
        new_grid[row_index][col_index] = letter
        return SudokuPuzzle(new_grid)


if __name__ == '__main__':
    # Note: the doctest of 'extensions' currently fails. See Part 1.
    import doctest
    doctest.testmod()

    # Here is a bigger Sudoku puzzle
    big = SudokuPuzzle(
        [['E', 'C', '', '', 'G', '', '', '', ''],
         ['F', '', '', 'A', 'I', 'E', '', '', ''],
         ['', 'I', 'H', '', '', '', '', 'F', ''],
         ['H', '', '', '', 'F', '', '', '', 'C'],
         ['D', '', '', 'H', '', 'C', '', '', 'A'],
         ['G', '', '', '', 'B', '', '', '', 'F'],
         ['', 'F', '', '', '', '', 'B', 'H', ''],
         ['', '', '', 'D', 'A', 'I', '', '', 'E'],
         ['', '', '', '', 'H', '', '', 'G', 'I']]
    )
    print(big)
