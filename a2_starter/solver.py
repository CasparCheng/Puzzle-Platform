# Assignment 2 - Puzzle Game
#
# CSC148 Summer 2017, University of Toronto
# ---------------------------------------------
"""This module contains functions responsible for solving a puzzle.

This module can be used to take a puzzle and generate one or all
possible solutions. It can also generate hints for a puzzle (see Part 4).
"""
from puzzle import Puzzle
from sudoku_puzzle import SudokuPuzzle
from word_ladder_puzzle import WordLadderPuzzle


def solve(puzzle, verbose=False):
    """Return a solution of the puzzle.

    Even if there is only one possible solution, just return one of them.
    If there are no possible solutions, return None.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds a solution.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: Puzzle | None

    >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
    ['', 'D', '', ''], ['', '', '', '']])
    >>> print(solve(s))
      01|23
     ------
    0|AB|CD
    1|DC|BA
     ------
    2|BD|AC
    3|CA|DB
    <BLANKLINE>
    >>> w = WordLadderPuzzle('ye', 'ac')
    >>> print(solve(w))
    ye be bb ab ac
    """
    # if the puzzle has been solved
    if puzzle.is_solved():
        # get the puzzle
        return puzzle
    # loop the list of all possible moves according to the current state
    for state in puzzle.extensions():
        # recursively get the new state
        state_new = solve(state, verbose)
        # if the new state exist
        if state_new:
            # if it is in verbose mode
            if verbose:
                # print the state
                print(state)
            return state_new


def solve_complete(puzzle, verbose=False):
    """Return all solutions of the puzzle.

    Return an empty list if there are no possible solutions.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds all solutions.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: list[Puzzle]

    >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
    ['', 'D', '', ''], ['', '', '', '']])
    >>> for x in solve_complete(s):
    ...     print(x)
      01|23
     ------
    0|AB|CD
    1|DC|BA
     ------
    2|BD|AC
    3|CA|DB
    <BLANKLINE>
      01|23
     ------
    0|AB|CD
    1|DC|BA
     ------
    2|CD|AB
    3|BA|DC
    <BLANKLINE>
    """
    # create a new empty list
    result = []
    # if the puzzle has been solved
    if puzzle.is_solved():
        # add the puzzle to the new list
        result = [puzzle]
    # otherwise
    else:
        # loop the list of all possible moves according to the current state
        for state in puzzle.extensions():
            # recursively get the new state
            states_new = solve_complete(state, verbose)
            # if the new state exist
            if states_new:
                # if in the verbose mode
                if verbose:
                    # print the state
                    print(state)
                # add the new state puzzle to the new list
                result += states_new

    return result


def hint_by_depth(puzzle, n):
    """Return a hint for the given puzzle state.

    Precondition: n >= 1.

    If <puzzle> is already solved, return the string Already at a solution!
    If <puzzle> cannot lead to a solution or
    other valid state within <n> moves,
    return the string ’No possible extensions!’

    @type puzzle: Puzzle
    @type n: int
    @rtype: str

    >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
    ['', 'D', '', ''], ['', '', '', '']])
    >>> print(hint_by_depth(s, 1))
    (2, 0) -> B
    >>> print(hint_by_depth(s, 100))
    (2, 0) -> B
    >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
    ['C', 'D', 'A', 'B'], ['B', 'A', 'D', 'C']])
    >>> print(hint_by_depth(s, 1))
    Already at a solution!
    >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
    ['', 'D', 'C', 'B'], ['D', 'A', 'A', 'A']])
    >>> print(hint_by_depth(s, 1))
    No possible extensions!
    >>> w = WordLadderPuzzle('ye', 'ac')
    >>> print(hint_by_depth(w, 1))
    be
    >>> print(hint_by_depth(w, 100))
    be
    >>> w = WordLadderPuzzle('ye', 'ac', ['ye', 'be', 'bb', 'ab', 'ac'])
    >>> print(hint_by_depth(w, 1))
    Already at a solution!
    >>> w = WordLadderPuzzle('aaaaaaaaaaa', 'ac')
    >>> print(hint_by_depth(w, 1))
    No possible extensions!
    """
    # if the puzzle has been solved
    if puzzle.is_solved():
        # return the message
        return "Already at a solution!"

    def helper(puz, m):
        """Return 2 if solution found or
        1 if only valid state found or None if otherwise
        in m moves

        @type puzzle: Puzzle
        @type m: int
        @rtype: int | None
        """
        # if the puzzle has been solved
        if puz.is_solved():
            return 2
        # if the move is 0
        if m == 0:
            return 1
        # define a result as none
        result = None
        # loop the list of all possible moves
        for state in puz.extensions():
            # recursively get the number of possible depth within m - 1 moves
            x = helper(state, m - 1)
            # if x exist
            if x:
                # if x is 2
                if x == 2:
                    return 2
                # otherwise result is 1
                result = 1
        return result
    # define a result as None
    result = None
    # loop the list of all possible moves
    for state in puzzle.extensions():
        # call the helper to get the number of possible depth within n-1 moves
        x = helper(puzzle, n - 1)
        # if x exist
        if x:
            # if x is 2
            if x == 2:
                # compare the two states
                return puzzle.compare(state)
            # if the result does not exist
            if not result:
                # the result is current state
                result = state
    # if result exist
    if result:
        # compare the two puzzle
        return puzzle.compare(result)
    # otherwise return the erroe message
    return "No possible extensions!"


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    from sudoku_puzzle import SudokuPuzzle
    s = SudokuPuzzle([['', '', '', ''],
                      ['', '', '', ''],
                      ['C', 'D', 'A', 'B'],
                      ['A', 'B', 'C', 'D']])

    solution = solve(s)
    print(solution)
