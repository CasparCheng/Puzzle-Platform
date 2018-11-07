# Assignment 2 - Puzzle Game
#
# CSC148 Summer 2017, University of Toronto
# ---------------------------------------------
"""Word ladder module.

Your task is to complete the implementation of this class so that
you can use it to play Word Ladder in your game program.

Rules of Word Ladder
--------------------
1. You are given a start word and a target word (all words in this puzzle
   are lowercase).
2. Your goal is to reach the target word by making a series of *legal moves*,
   beginning from the start word.
3. A legal move at the current word is to change ONE letter to get
   a current new word, where the new word must be a valid English word.

The sequence of words from the start to the target is called
a "word ladder," hence the name of the puzzle.

Example:
    Start word: 'make'
    Target word: 'cure'
    Solution:
        make
        bake
        bare
        care
        cure

    Note that there are many possible solutions, and in fact a shorter one
    exists for the above puzzle. Do you see it?

Implementation details:
- We have provided some starter code in the constructor which reads in a list
  of valid English words from wordsEn.txt. You should use this list to
  determine what moves are valid.
- **WARNING**: unlike Sudoku, Word Ladder has the possibility of getting
  into infinite recursion if you aren't careful. The puzzle state
  should keep track not just of the current word, but all words
  in the ladder. This way, in the 'extensions' method you can just
  return the possible new words which haven't already been used.
"""
from puzzle import Puzzle


CHARS = 'abcdefghijklmnopqrstuvwyz'


class WordLadderPuzzle(Puzzle):
    """A word ladder puzzle."""
    # TODO: add to this list of private attributes!
    # === Private attributes ===
    # @type _words: list[str]
    #     List of allowed English words
    # @type _hashed_words: set(list[str])
    #     set of list of allowed English words
    # @type _start: str
    #     start word
    # @type _target: str
    #     target word
    # @type _hist: list
    #     list of hist

    def __init__(self, start, target, hist=[]):
        """Create a new word ladder puzzle with given start and target words.

        Note: you may add OPTIONAL arguments to this constructor,
        but you may not change the purpose of <start> and <target>.

        @type self: WordLadderPuzzle
        @type start: str
        @type target: str
        @type hist: list
        @rtype: None
        """
        # Code to initialize _words - you don't need to change this.
        self._words = []
        with open('wordsEn.txt') as wordfile:
            for line in wordfile:
                self._words.append(line.strip())

        # TODO: Complete the constructor.

        # initialize the hashed words as the set of _words
        self._hashed_words = set(self._words)
        # initialize the start word
        self._start = start
        # initialize the target word
        self._target = target
        # if the hist exist
        if hist:
            # copy the list of hist
            self._hist = hist.copy()
        # otherwise
        else:
            # the wordladder hist is the list of start word
            self._hist = [start]

    def __str__(self):
        """Please do not change this
        @type self: WordLadderPuzzle
        @rtype: str

        >>> w = WordLadderPuzzle('ye', 'ac')
        >>> print(w)
        ye
        >>> w = WordLadderPuzzle('ye', 'ac', ['ye', 'be'])
        >>> print(w)
        ye be
        """
        return ' '.join(self._hist)

    def is_solved(self):
        """Return whether <self> is solved.

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> w = WordLadderPuzzle('ye', 'ac')
        >>> w.is_solved()
        False
        >>> w = WordLadderPuzzle('ye', 'ac', ['ye', 'be', 'bb', 'ab', 'ac'])
        >>> w.is_solved()
        True
        """
        # check whether the last element is the target word
        return self._hist[-1] == self._target

    def extensions(self):
        """Return a list of possible new states after a valid move.

        The valid move must change exactly one character of the
        current word, and must result in an English word stored in
        self._words.

        You should *not* perform any moves which produce a word
        that is already in the ladder.

        The returned moves should be sorted in alphabetical order
        of the produced word.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]

        >>> w = WordLadderPuzzle('ye', 'ac')
        >>> lst = list(w.extensions())
        >>> len(lst)
        10
        >>> print(lst[0])
        ye be
        >>> print(lst[1])
        ye de
        >>> print(lst[2])
        ye he
        >>> print(lst[3])
        ye ie
        >>> print(lst[4])
        ye me
        >>> print(lst[5])
        ye ne
        >>> print(lst[6])
        ye re
        >>> print(lst[7])
        ye se
        >>> print(lst[8])
        ye we
        >>> print(lst[9])
        ye yr
        """
        # if the puzzle has been solved
        if self.is_solved():
            # return the empty list
            return []
        # otherwise loop the possible moves and add it to the wordladder
        # then return the list of possible new states
        return [self._extend(word)
                for word in self._possible_words()]

    def move(self, move):
        """Return a new puzzle state specified by making the given move.

        Raise a ValueError if <move> represents an invalid move.
        Do not change the state of <self>. This is not a mutating method!

        @type self: WordLadderPuzzle
        @type move: str
        @rtype: WordLadderPuzzle

        >>> w = WordLadderPuzzle('ye', 'ac')
        >>> print(w.move('be'))
        ye be
        >>> try:
        ...   w.move('xxx')
        ... except Exception as e:
        ...   print(e)
        Incorrect word length!
        >>> try:
        ...   w.move('ye')
        ... except Exception as e:
        ...   print(e)
        Repetitive word found!
        >>> try:
        ...   w.move('by')
        ... except Exception as e:
        ...   print(e)
        Incorrect number of changed letters!
        >>> try:
        ...   w.move('yy')
        ... except Exception as e:
        ...   print(e)
        Illegal word!
        """
        # get the new state after move
        state_new = move.strip()
        # get the state by getting the last element in the hist
        state = self._hist[-1]
        # if the new state is not equal to the state
        if len(state_new) != len(state):
            # raise the value error
            raise ValueError('Incorrect word length!')
        # if the new state is in the hist
        if state_new in self._hist:
            # raise the value error
            raise ValueError('Repetitive word found!')
        # define the number of changes started with 0
        n_changes = 0
        # loop the length of state
        for index in range(len(state)):
            # if the state is not equal to the new state in the current index
            if state[index] != state_new[index]:
                # number of changes add 1
                n_changes += 1
        # if the number of changes do not happen just once
        if n_changes != 1:
            # raise the value error
            raise ValueError('Incorrect number of changed letters!')
        # if the new state is not in the hashed words
        if state_new not in self._hashed_words:
            # raise the value error
            raise ValueError('Illegal word!')
        # return the puzzle after given moves
        return self._extend(state_new)

    def compare(self, state):
        """Return a move obtained by comparing with <state>
        or None if no differences found

        Precondition: <state> should be one move advanced.

        @type self: WordLadderPuzzle
        @type state: WordLadderPuzzle
        @rtype: str | None

        >>> w = WordLadderPuzzle('ye', 'ac')
        >>> w1 = WordLadderPuzzle('ye', 'ac', ['ye', 'be'])
        >>> w.compare(w1)
        'be'
        """
        return state._hist[-1]

    # ------------------------------------------------------------------------
    # Helpers for method 'extensions'
    # ------------------------------------------------------------------------
    def _possible_words(self):
        """Return a list of the possible letters for a position.

        The returned letters must be a subset of the available letters.
        The returned list should be sorted in alphabetical order.

        @type self: WordLadderPuzzle
        @type index: int
        @rtype: list[str]

        >>> w = WordLadderPuzzle('ye', 'ac')
        >>> w._possible_words()
        ['be', 'de', 'he', 'ie', 'me', 'ne', 're', 'se', 'we', 'yr']
        """
        # get the acaliable words
        avaliable = self._hashed_words - set(self._hist[:-1])
        # get the final state in the hist
        state = list(self._hist[-1])
        # create a new empty list as result
        result = []
        # loop the length of the puzzle state
        for index in range(len(state)):
            # get the letters in the state
            letters = set(CHARS) - set([state[index]])
            # loop the letters
            for let in letters:
                # define a new state as the list of the current state
                state_new = list(state)
                # change the new state to the letter at the index position
                state_new[index] = let
                state_new = ''.join(state_new)
                # if the new state is in the avaliable words
                if state_new in avaliable:
                    # add it to the result
                    result.append(state_new)

        # return the sorted result
        return sorted(result)

    def _extend(self, state):
        """Return a new word ladder obtained after one move.

        The new puzzle is identical to <self>, except that it has
        a new word appended in history.

        'state' must be a proper/legal word.

        @type self: WordLadderPuzzle
        @type state: WordLadderPuzzle
        @rtype: WordLadderPuzzle

        >>> w = WordLadderPuzzle('ye', 'ac')
        >>> print(w._extend('be'))
        ye be
        """
        return WordLadderPuzzle(
            self._start, self._target, self._hist + [state])


if __name__ == '__main__':
    import doctest
    doctest.testmod()
