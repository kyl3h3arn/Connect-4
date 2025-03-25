# 🎮 Connect Four AI Game (Minimax & Alpha-Beta)
**UNC Charlotte - ITCS 5153: Applied AI - Fall 2024**  
**Lab 3: Adversarial Search / Game Playing**  
**Student ID: 801115708**

This project is a graphical implementation of the classic **Connect Four** game. It features two AI agents built using the **Minimax** and **Alpha-Beta Pruning** algorithms. The game is developed with **Pygame** and allows a human player to challenge an AI.

---

## 🧠 Features

- 🎨 Interactive GUI using Pygame
- 🤖 Two AI algorithms to choose from:
  - Minimax
  - Alpha-Beta Pruning
- 📊 Node exploration stats printed in the terminal
- 🧠 Depth-limited search for performance
- 🕹️ Game controls:
  - New Game
  - Restart
  - Exit
  - Algorithm Selection

---

## 🗂️ File Structure

| File Name              | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `main_801115708.py`    | Main entry point for launching the game                                    |
| `display_801115708.py` | Contains the GUI logic using Pygame: drawing board, buttons, game loop      |
| `logic_801115708.py`   | Core game logic: rules, state representation, move validation               |
| `search_801115708.py`  | AI implementations: Minimax and Alpha-Beta Pruning with depth cutoff        |

---

## 💻 Requirements

- Python 3.x
- [Pygame](https://www.pygame.org/)
- [NumPy](https://numpy.org/)
