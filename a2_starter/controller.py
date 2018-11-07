# Assignment 2 - Puzzle Game
#
# CSC148 Summer 2017, University of Toronto
# ---------------------------------------------
"""Module containing the Controller class."""
from view import TextView, WebView
from puzzle import Puzzle
from solver import solve, solve_complete, hint_by_depth


class MoveTreeCore:
    """Class used as core of MoveTree to represent the tree node

    # === Private Attributes ===
    # @type _state: Puzzle
    #     The associated puzzle
    # @type _move: str
    #     The move player made
    # @type _parent: MoveTreeCore
    #     The parent node
    # @type _children: list<MoveTreeCore>
    #     The child nodes
    """

    def __init__(self, state, move='', parent=None):
        """Create a new node

        @type state: Puzzle
        @type mode: str
        @type parent: MoveTreeCore | None
        @rtype: None
        """
        # initialize the state
        self._state = state
        # initialize the move
        self._move = move
        # initialize the parent
        self._parent = parent
        # initialize the children as an empty list
        self._children = []

    def do(self, state, move):
        """Return a node advanced by the specified move

        @type state: Puzzle
        @type mode: str
        @rtype: MoveTreeCore
        """
        # loop the children of the tree with index and element
        for i, child in enumerate(self._children):
            # if the move is equal to the child's move
            if move == child._move:
                # return the matched index of children
                return self._children[i]
        # create a tree as the child
        child = MoveTreeCore(state, move, self)
        # append the new child to the children list
        self._children.append(child)
        return child

    def undo(self):
        """Return a parent node if there is one otherwise None

        @type self: MoveTreeCore
        @rtype: MoveTreeCore | None
        """
        # if the parent exists
        if self._parent:
            return self._parent

    def attempts(self):
        """Return child nodes if there are any otherwise None

        @type self: MoveTreeCore
        @rtype: MoveTreeCore | None
        """
        # if the children exist
        if self._children:
            return self._children


class MoveTree:
    """Class used as wrapper of MoveTreeCore to represent the tree structure

    # === Private Attributes ===
    # @type _movetreecore: MoveTreeCore
    #     The associated MoveTreeCore
    """

    def __init__(self, state):
        """Create a new tree

        @type state: Puzzle
        @rtype: None
        """
        # Initialize the movetreecore with the given state
        self._movetreecore = MoveTreeCore(state)

    def do(self, state, move):
        """Advance tree by the specified move

        @type state: Puzzle
        @type mode: str
        @rtype: None
        """
        # recursively do the move
        self._movetreecore = self._movetreecore.do(state, move)

    def undo(self):
        """Return the message and state after undo the tree

        @type self: MoveTree
        @rtype: (str, Puzzle)
        """
        # resursively undo the move
        x = self._movetreecore.undo()
        # if the x exist
        if x:
            # define the movetreecore with x
            self._movetreecore = x
            # return the string of state and the state after undo the tree
            return str(x._state), x._state
        # else return the message and the state
        return 'No steps to undo!', self._movetreecore._state

    def attempts(self):
        """Return message by scan the attempts in tree

        @type self: MoveTree
        @rtype: str
        """
        # recursively do the movetreecore attempts
        xs = self._movetreecore.attempts()
        # if the xs exist
        if xs:
            # create an empty list
            result = []
            # loop the xs
            for x in xs:
                # append the move and the current state of x
                result.append(x._move + '\n' + str(x._state))
            return '\n'.join(result)
        # otherwise no attempts found
        return 'No attemps found!'


class Controller:
    """Class responsible for connection between puzzles and views.

    You may add new *private* attributes to this class to help you
    in your implementation.
    """
    # === Private Attributes ===
    # @type _puzzle: Puzzle
    #     The puzzle associated with this game controller
    # @type _view: View
    #     The view associated with this game controller

    def __init__(self, puzzle, mode='text'):
        """Create a new controller.

        <mode> is either 'text' or 'web', representing the type of view
        to use.

        By default, <mode> has a value of 'text'.

        @type puzzle: Puzzle
        @type mode: str
        @rtype: None
        """
        self._puzzle = puzzle
        if mode == 'text':
            self._view = TextView(self)
        elif mode == 'web':
            self._view = WebView(self)
        else:
            raise ValueError()

        # Create the tree data structure to record moves
        self._movetree = MoveTree(puzzle)
        # Start the game.
        self._view.run()

    def state(self):
        """Return a string representation of the current puzzle state.

        @type self: Controller
        @rtype: str
        """
        return str(self._puzzle)

    def act(self, action):
        """Run an action represented by string <action>.

        Return a string representing either the new state or an error message,
        and whether the program should end.

        @type self: Controller
        @type action: str
        @rtype: (str, bool)
        """
        # TODO: Add to this method to handle different actions.

        # if the action command is 'EXIT'
        if action == ':EXIT':
            # return empty string and the program should end
            return ('', True)
        # else if the action command is 'SOLVE'
        elif action == ':SOLVE':
            # solve the puzzle
            state = solve(self._puzzle)
            # if the state exists
            if state:
                # return the solution, and the program should end
                return (str(state), True)
            # otherwise return the error message, the program should end
            return ('Failed to solve from this point!', True)
        # else if the action command is 'SOLVE-ALL'
        elif action == ':SOLVE-ALL':
            # get the all possible solution
            states = solve_complete(self._puzzle)
            # if the states exist
            if states:
                # return the all solutions in the correct format, and the
                # program should end
                return ('\n'.join(map(str, states)), True)
            # otherwise return the error message, and program should end
            return ('Failed to solve from this point!', True)
        # else if the action command let the program give hint
        elif action.startswith(':HINT'):
            # split the action command to the list of parts
            parts = action.split(' ')
            # if the length of parts are 2
            if len(parts) != 2:
                # return the error message for action, the program should
                # not end
                return ('Incorrect action format for hints!', False)
            # try the following firstly
            try:
                # get the index 1 of parts
                n = int(parts[1])
            # else raise value error
            except ValueError:
                # return the error message for action, the program
                # should not end
                return ('Incorrect action format for hints!', False)
            # if the n is less than 1
            if n < 1:
                # return the error message for action, the program should
                # not end
                return ('Incorrect action format for hints!', False)
            # otherwise get the hint by calling hint by depth function,
            # the program should not end
            return (hint_by_depth(self._puzzle, n), False)
        # if the action command is 'UNDO'
        elif action == ':UNDO':
            # return the string of the new current state and the current
            # state of puzzle
            result, self._puzzle = self._movetree.undo()
            # return the string of new current state and the program should
            # not end
            return (result, False)
        # else if the action command is 'ATTEMPTS'
        elif action == ':ATTEMPTS':
            # return the all resulting from the user made at the current state
            # and the program should not end
            return (self._movetree.attempts(), False)
        # if the action command is ':'
        elif action == ':':
            # return the current state of puzzle, and the program should
            # not end
            return (self.state(), False)
        # otherwise
        else:
            # try following
            try:
                # get the current state of puzzleafter given move
                state = self._puzzle.move(action)
            # else the value error
            except ValueError as e:
                # return the string of e, and the program should not end
                return (str(e), False)
            # update the puzzle after move
            self._puzzle = state
            # get the puzzle state by finding the node of move from tree
            self._movetree.do(state, action)
            # return the current puzzle state
            # and check whether it has been solved
            return (self.state(), state.is_solved())


if __name__ == '__main__':
    from sudoku_puzzle import SudokuPuzzle
    s = SudokuPuzzle([['', '', '', ''],
                      ['', '', '', ''],
                      ['C', 'D', 'A', 'B'],
                      ['A', 'B', 'C', 'D']])
    c = Controller(s)

    from word_ladder_puzzle import WordLadderPuzzle
    s = WordLadderPuzzle('ye', 'ac')
    c = Controller(s)
