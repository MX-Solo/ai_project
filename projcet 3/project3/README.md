# Othello Game with Minimax Algorithm

This project implements the classic board game Othello (also known as Reversi) using Python. It allows for two-player gameplay and also integrates the **Minimax** algorithm to provide an AI-based player. The game features a graphical board, alternating turns between two players, and a final score display.

## Table of Contents
1. [Project Structure](#project-structure)
2. [How to Run](#how-to-run)
3. [Game Rules](#game-rules)
4. [Code Overview](#code-overview)
5. [Agent (AI) Implementation](#agent-ai-implementation)
6. [Minimax Algorithm](#minimax-algorithm)

## Project Structure

The project consists of the following Python files:

- **`board.py`**: Contains the logic for the game board and managing valid moves.
- **`main.py`**: The entry point to start and play the game.
- **`minimax.py`**: Implements the minimax algorithm for AI decision-making.
- **`expectimax.py`**: Implements the expectimax algorithm for AI decision-making.
- **`player.py`**: Manages player interaction and moves.
- **`game.py`**: Manages the overall flow of the game, handling turns, checking the game state, and determining the winner.

## How to Run

To run this Othello game on your local machine:

1. import packages:
   ```bash
   pip install pygame
   ```
2. run the project
  ```
  python main.py
```
   


## Game rules

### `board.py`

The `Board` class manages the 8x8 Othello board. It includes methods for:

- **Displaying the board**: `display()`
- **Retrieving valid moves for a player**: `get_valid_moves()`
- **Placing a disc on the board**: `place_disc()`
- **Checking if the board is full**: `is_full()`
- **Calculating the score for both players**: `get_score()`

### `game.py`

The `Game` class manages the overall game loop and player interactions. It tracks which player's turn it is, checks if the game is over, and declares the winner. Key methods include:

- **`start()`**: Runs the main game loop until the game ends.
- **`switch_turns()`**: Alternates turns between players.
- **`is_game_over()`**: Determines if the game has finished.
- **`declare_winner()`**: Declares the winner based on the final score.

### `main.py`

This file serves as the entry point for running the game. It initializes the players (human or AI) and starts the game.

### `player.py`

The `Agent` class in this file represents the players in the game. The player can be either a human or an AI. The file manages the player’s color and the logic for making moves. For AI players, the minimax algorithm is used to decide the best move.

## Agent (AI) Implementation

Players can be human or AI-controlled. In the case of AI, the player uses the **Minimax** algorithm to make decisions. The minimax algorithm looks ahead several moves to evaluate potential game outcomes and tries to maximize the AI’s score while minimizing the opponent’s score.

### `Agent Class` in `player.py`

The `Agent` class:

- **Human players**: Provide their moves through user input.
- **AI players**: Make moves based on the Minimax algorithm, searching through possible board states to determine the best move.

## Minimax Algorithm

The minimax algorithm is implemented in the **`minimax.py`** file. It evaluates the board's state by simulating possible moves up to a certain depth and chooses the move that maximizes the player's advantage while minimizing the opponent's. This method makes the AI player challenging to defeat.

### Key Features:

- **Depth-limited search**: The algorithm considers moves up to a certain depth to make the decision process computationally feasible.
- **Score evaluation**: It evaluates the current board state to estimate the advantage for the player based on the number of discs controlled.
