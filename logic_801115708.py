# UNC Charlotte
# ITCS 5153 - Applied AI - Fall 2024
# Lab 3
# Adversarial Search / Game Playing
# This module implements the logic for the Connect Four game.
# Student ID: 801115708

from collections import namedtuple

# GameState namedtuple for holding state information
GameState = namedtuple('GameState', 'to_move, utility, board, moves')

class ConnectFour:
    """A Connect Four game where you can only make a move on the bottom
    row, or in a square directly above an occupied square."""

    def __init__(self, h=6, v=7, k=4):
        """Initialize a standard Connect Four game."""
        self.h = h  # Board height (6 rows)
        self.v = v  # Board width (7 columns)
        self.k = k  # Number of pieces in a row required to win
        # Initialize an empty board and a set of available moves
        moves = [(x, y) for x in range(1, h + 1) for y in range(1, v + 1)]
        self.initial = GameState(to_move=1, utility=0, board={}, moves=moves)

    def actions(self, state):
        """Return a list of valid moves for the current state."""
        valid_moves = [(row, col) for row, col in state.moves
                       if row == self.h or (row + 1, col) in state.board]
        return valid_moves

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move  # Update board with the player's piece
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=(-state.to_move), utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 1 else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def compute_utility(self, board, move, player):
        """If the move leads to a win for the player, return 1; else return 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or  # Horizontal
                self.k_in_row(board, move, player, (1, 0)) or  # Vertical
                self.k_in_row(board, move, player, (1, -1)) or  # Diagonal
                self.k_in_row(board, move, player, (1, 1))):  # Anti-diagonal
            return 1 if player == 1 else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta):
        """Return True if there is a line through move on board for player."""
        (delta_x, delta_y) = delta
        x, y = move
        n = 0  # Number of moves in row
        # Check in both directions
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Since the move itself is counted twice
        return n >= self.k

    def display(self, state):
        """Print or otherwise display the state."""
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()
        print()