# UNC Charlotte
# ITCS 5153 - Applied AI - Fall 2024
# Lab 3
# Adversarial Search / Game Playing
# This module implements the Pygame interface for Connect Four.
# Student ID: 801115708

import pygame
import sys
import time
from search_801115708 import minmax_player, alpha_beta_player

# Pygame display constants
WINDOW_WIDTH, WINDOW_HEIGHT = 700, 750  # Increase height for algo selection buttons
CELL_SIZE = 100
RADIUS = CELL_SIZE // 2 - 5
GRID_COLOR = (0, 0, 255)
BG_COLOR = (255, 255, 255)
PLAYER_ONE_COLOR = (255, 0, 0)  # Red
PLAYER_TWO_COLOR = (255, 255, 0)  # Yellow
EMPTY_COLOR = (0, 0, 0)
BUTTON_COLOR = (0, 0, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
POPUP_BG_COLOR = (255, 255, 255)
POPUP_TEXT_COLOR = (0, 0, 0)

# Button dimensions
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 40
BUTTON_Y = 10  # Position buttons at the top of the window

# Initialize the board dimensions
ROWS = 6
COLS = 7

# Add additional y-offset for the algorithm selection buttons
ALGO_BUTTON_Y = BUTTON_Y + BUTTON_HEIGHT + 10  # Position algorithm buttons below control buttons

def draw_buttons(screen):
    """Draws the control buttons for new game, restart, and exit."""
    font = pygame.font.Font(None, 36)

    # New Game Button
    new_game_rect = pygame.Rect(10, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, new_game_rect)
    new_game_text = font.render('New Game', True, BUTTON_TEXT_COLOR)
    screen.blit(new_game_text, (new_game_rect.x + 20, new_game_rect.y + 5))

    # Restart Button
    restart_rect = pygame.Rect(170, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, restart_rect)
    restart_text = font.render('Restart', True, BUTTON_TEXT_COLOR)
    screen.blit(restart_text, (restart_rect.x + 35, restart_rect.y + 5))

    # Exit Button
    exit_rect = pygame.Rect(330, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, exit_rect)
    exit_text = font.render('Exit', True, BUTTON_TEXT_COLOR)
    screen.blit(exit_text, (exit_rect.x + 50, exit_rect.y + 5))

    return new_game_rect, restart_rect, exit_rect

def draw_algo_buttons(screen):
    """Draws the algorithm selection buttons for Minimax and Alpha-Beta."""
    font = pygame.font.Font(None, 36)

    # Minimax Button
    minimax_rect = pygame.Rect(10, ALGO_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, minimax_rect)
    minimax_text = font.render('Minimax', True, BUTTON_TEXT_COLOR)
    screen.blit(minimax_text, (minimax_rect.x + 10, minimax_rect.y + 5))

    # Alpha-Beta Button
    alpha_beta_rect = pygame.Rect(170, ALGO_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, alpha_beta_rect)
    alpha_beta_text = font.render('Alpha-Beta', True, BUTTON_TEXT_COLOR)
    screen.blit(alpha_beta_text, (alpha_beta_rect.x + 5, alpha_beta_rect.y + 5))

    return minimax_rect, alpha_beta_rect

def draw_board(screen, state):
    """Draws the game board on the Pygame screen."""
    board_top_y = ALGO_BUTTON_Y + BUTTON_HEIGHT + 20  # 20px padding below algo buttons

    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, GRID_COLOR, (c * CELL_SIZE, r * CELL_SIZE + board_top_y, CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(screen, EMPTY_COLOR,
                               (int(c * CELL_SIZE + CELL_SIZE / 2), int(r * CELL_SIZE + board_top_y + CELL_SIZE / 2)),
                               RADIUS)

    for (x, y), value in state.board.items():
        row = x - 1
        col = y - 1
        draw_row = row
        color = PLAYER_ONE_COLOR if value == 1 else PLAYER_TWO_COLOR
        pygame.draw.circle(screen, color,
                           (int(col * CELL_SIZE + CELL_SIZE / 2),
                            int(draw_row * CELL_SIZE + board_top_y + CELL_SIZE / 2)),
                           RADIUS)

def update_screen(screen, state):
    """Draw all elements on the screen."""
    screen.fill(BG_COLOR)
    draw_board(screen, state)
    draw_buttons(screen)
    draw_algo_buttons(screen)
    pygame.display.update()

def get_move_from_click(pos, game, state):
    """Converts a click position to a game move (column)."""
    x, y = pos
    board_top_y = ALGO_BUTTON_Y + BUTTON_HEIGHT + 20
    if y < board_top_y or y > board_top_y + ROWS * CELL_SIZE:
        return None
    col = x // CELL_SIZE + 1
    for row in range(game.h, 0, -1):
        if (row, col) not in state.board:
            return (row, col)
    return None

def show_winner_popup(screen, winner):
    """Displays a popup declaring the winner."""
    font = pygame.font.Font(None, 72)
    popup_text = f"{winner} Wins!"
    popup_surface = font.render(popup_text, True, POPUP_TEXT_COLOR)
    popup_rect = popup_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    pygame.draw.rect(screen, POPUP_BG_COLOR, popup_rect.inflate(20, 20))
    screen.blit(popup_surface, popup_rect)
    pygame.display.update()
    time.sleep(2)

def run_game(game_class):
    """Main Pygame loop to run the Connect Four interface."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Connect Four")

    game = game_class()
    state = game.initial
    human_turn = True
    running = True
    game_over = False
    ai_algorithm = None

    update_screen(screen, state)
    print("Please select an algorithm (Minimax or Alpha-Beta) to begin.")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                new_game_button, restart_button, exit_button = draw_buttons(screen)

                if exit_button.collidepoint(pos):
                    print("Exiting Game")
                    running = False
                    break

                if ai_algorithm is None:
                    minimax_button, alpha_beta_button = draw_algo_buttons(screen)
                    if minimax_button.collidepoint(pos):
                        ai_algorithm = minmax_player
                        print("Algorithm Selected: Minimax")
                    elif alpha_beta_button.collidepoint(pos):
                        ai_algorithm = alpha_beta_player
                        print("Algorithm Selected: Alpha-Beta")

                if ai_algorithm:
                    if new_game_button.collidepoint(pos):
                        game = game_class()
                        state = game.initial
                        human_turn = True
                        game_over = False
                        ai_algorithm = None
                        print("New Game Started. Please select an algorithm.")
                        update_screen(screen, state)

                    elif restart_button.collidepoint(pos):
                        state = game.initial
                        human_turn = True
                        game_over = False
                        update_screen(screen, state)

                    elif not game_over and human_turn:
                        move = get_move_from_click(pos, game, state)
                        if move and move in game.actions(state):
                            state = game.result(state, move)
                            update_screen(screen, state)
                            if game.terminal_test(state):
                                print("Game Over! Human Wins!")
                                show_winner_popup(screen, "Human")
                                game_over = True
                            else:
                                human_turn = False

                elif not game_over and human_turn:
                    print("Please select an algorithm before making a move!")

        if not human_turn and not game_over and ai_algorithm:
            start_time = time.time()
            print("AI is thinking...")

            ai_move = ai_algorithm(game, state)

            state = game.result(state, ai_move)
            update_screen(screen, state)
            elapsed_time = time.time() - start_time

            minutes, seconds = divmod(elapsed_time, 60)
            milliseconds = (elapsed_time - int(elapsed_time)) * 1000

            print(
                f"AI moved to {ai_move} in {int(minutes)} minutes, {int(seconds):02} seconds, and {int(milliseconds):03} milliseconds.")

            if game.terminal_test(state):
                print("Game Over! AI Wins!")
                show_winner_popup(screen, "AI")
                game_over = True
            else:
                human_turn = True

    pygame.quit()
    sys.exit()
