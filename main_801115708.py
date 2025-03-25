# UNC Charlotte
# ITCS 5153 - Applied AI - Fall 2024
# Lab 3
# Adversarial Search / Game Playing
# This module runs the main loop for the Connect Four game.
# Student ID: 801115708

from logic_801115708 import ConnectFour
from display_801115708 import run_game

def main():
    # Run the Pygame interface with the game logic
    run_game(ConnectFour)

if __name__ == "__main__":
    main()
