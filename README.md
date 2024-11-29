# TerminalChess

A Python-based library for managing and playing chess games. This library offers a robust implementation of chess game mechanics using graph algorithms, Dynamic Programming, and OOP. Features include board management, move validation, check/checkmate detection, and user input handling. 

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Key Classes and Functions](#key-classes-and-functions)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)

## Features

- **Game State Management**: Keep track of the board, pieces, moves, and game status.
- **Rules Enforcement**: Validates moves according to chess rules, including special moves like castling and en passant.
- **Check and Checkmate Detection**: Identifies when a king is in check or checkmate.
- **Undo and Replay**: Supports undo functionality to revert moves and analyze gameplay.
- **Interactive Gameplay**: Allows users to play against each other through terminal-based input.

## Requirements

- Python 3.8 or higher
- Dependencies: None beyond Python's standard library

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/chess-game-library.git
cd chess-game-library
```
## Usage
### Running the Game
To start a chess game:
```bash
python main.py
```
## Key Classes and Functions
- `Square`: Represents a square on the chessboard.
- `Piece`: Represents individual chess pieces and their behaviors.
- `update_all`: Updates the board, available moves, and capturable pieces.
- `assess_check` and `assess_checkmate`: Determines whether a player is in check or checkmate.
- `one_turn`: Handles user input and validates moves.
- `undo`: Reverts the game to a previous state.
- `play`: Initiates and manages the game flow.

## Project Structure
```bash
chess/
├── objects/
│   ├── elements.py        # Definitions for Square, Piece, and other chess elements
│   ├── functions.py       # Utility functions like user input handling
│   ├── board.py           # The main Board object that handles all gamestates, rules, and memory
├── main.py                # Entry point for running the chess game
├── README.md              # Documentation for the repository
```

## Roadmap
- Prevent players from making moves that put themselves in check
- Add *en passant*, *draw by repetition*, and *the 50 move rule*
- Implement AI for single-player mode.
- Add GUI support using a Python GUI library (e.g., PyQt, tkinter).
- Support additional chess variants (e.g., Fischer Random Chess).
- Improve performance of board state updates.
