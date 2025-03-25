# UNC Charlotte
# ITCS 5153 - Applied AI - Fall 2024
# Lab 3
# Adversarial Search / Game Playing
# This module implements the Alpha-Beta pruning and MiniMax algorithms for Connect Four.
# Student ID: 801115708

import numpy as np

# Initialize counters to track nodes explored
nodes_explored = 0
total_nodes_explored = 0  # Cumulative total across the entire game

# Alpha-Beta Pruning with Depth Cutoff
def alpha_beta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        global nodes_explored
        nodes_explored += 1  # Increment node count

        if cutoff_test(state, depth):
            return eval_fn(state)

        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        global nodes_explored
        nodes_explored += 1  # Increment node count

        if cutoff_test(state, depth):
            return eval_fn(state)

        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Define the cutoff test correctly
    cutoff_test = cutoff_test or (lambda state, depth: (depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_action = None

    # Iterate through possible actions and determine the best action based on min_value
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


# Wrapper function to easily use Alpha-Beta pruning as a player agent
def alpha_beta_player(game, state, depth=4):
    """A player function for the AI using Alpha-Beta pruning with a depth cutoff."""
    global nodes_explored, total_nodes_explored
    nodes_explored = 0  # Reset node count for each AI move
    best_move = alpha_beta_cutoff_search(state, game, d=depth)
    total_nodes_explored += nodes_explored  # Update cumulative count
    print(f"AI explored {nodes_explored} nodes this turn using Alpha-Beta pruning.")
    print(f"Total nodes explored so far: {total_nodes_explored} nodes.")
    return best_move


# Minimax Algorithm with Depth Cutoff
def minmax_decision(state, game, depth=4):
    """Calculate the best move using Minimax with a depth limitation."""
    player = game.to_move(state)

    def max_value(state, current_depth):
        global nodes_explored
        nodes_explored += 1  # Increment node count

        if game.terminal_test(state) or current_depth == 0:
            return game.utility(state, player)

        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), current_depth - 1))
        return v

    def min_value(state, current_depth):
        global nodes_explored
        nodes_explored += 1  # Increment node count

        if game.terminal_test(state) or current_depth == 0:
            return game.utility(state, player)

        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), current_depth - 1))
        return v

    # Select best move based on the Minimax value
    best_move = max(game.actions(state), key=lambda a: min_value(game.result(state, a), depth - 1))
    return best_move

# Wrapper function to use Minimax as an AI player
def minmax_player(game, state, depth=4):
    """A player function for the AI using Minimax with a depth cutoff."""
    global nodes_explored, total_nodes_explored
    nodes_explored = 0  # Reset node count for each AI move
    best_move = minmax_decision(state, game, depth)
    total_nodes_explored += nodes_explored  # Update cumulative count
    print(f"AI explored {nodes_explored} nodes this turn using Minimax.")
    print(f"Total nodes explored so far: {total_nodes_explored} nodes.")
    return best_move