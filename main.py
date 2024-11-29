"""
This module contains the `Board` class, which represents the state of a chess game. 

The `Board` class manages the layout of the chessboard, piece movements, game rules, and 
player turns. It provides methods to update the board, validate moves, 
and assess the current game state.

Key functionality includes:
- Handling player turns and user input.
- Moving pieces while enforcing the rules of chess.
- Checking for check, checkmate, stalemate, and other game-ending conditions.
- Supporting undo operations to reverse previous moves.
- Managing castling conditions for both players.

Usage:
    To use the `Board` class, import it and instantiate an object of the class to 
    interact with the chess game.

Example:
    from chess.objects.board import Board
    game = Board()
    game.start_game()
"""
from objects.board import Board
board = Board()
board.play()
