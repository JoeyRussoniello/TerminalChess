"""
This module contains functions and classes related to managing the game state in a chess game.

It includes the logic for checking the game conditions (checkmate, check, etc.), updating the board,
and handling player turns. The module uses `copy` for making deep copies of the game state and
relies on other chess-specific objects such as `Square` and `Piece`.

Dependencies:
- `copy`: Provides the `deepcopy` function to create independent copies of the game state.
- `Square`: A class representing the squares on the chessboard.
- `Piece`: A class representing the chess pieces and their attributes.
- `take_user_input`: A function to capture user input for making moves.

Functions:
- assess_checkmate(turn): Determines if the current player is in checkmate.
- assess_check(turn): Checks if the current player’s king is in check.
- update_all(): Updates the game state, including piece positions and available moves.
- turn(color): Manages the player's turn, validating moves and handling the game flow.
- game_loop(turn): The main game loop that alternates turns and checks for game-ending conditions. 
    Called in Board.play()
- undo(): Reverts the game to the previous state based on the history of moves.
- play(): Starts the game and manages multiple rounds or a continuous playthrough.
"""
import copy
from .elements import Square,Piece
from .functions import take_user_input
class Board:
    def __init__(self,board = None):
        board_arr = []
        #Create an 8 x 8 empty board
        for i in range(8):
            row_arr = []
            for j in range(8):
                row_arr.append(Square(self,(i,j)))
            board_arr.append(row_arr)
        
        #Connect all squares and their pointers
        for i in range(8):
            for j in range(8):
                square = board_arr[i][j]
                if j >= 1:
                    square.left = board_arr[i][j-1]
                if j <= 6:
                    square.right = board_arr[i][j+1]
                if i >= 1:
                    square.up = board_arr[i-1][j]
                if i <= 6:
                    square.down = board_arr[i+1][j]
        
        if not board:
            board = [
                ['wr','wn','wb','wq','wk','wb','wn','wr'],
                ['wp','wp','wp','wp','wp','wp','wp','wp'],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['bp','bp','bp','bp','bp','bp','bp','bp'],
                ['br','bn','bb','bq','bk','bb','bn','br']
            ]
        
        piece_arr = []
        for i in range(8):
            piece_row = []
            for j in range(8):
                square = board_arr[i][j]
                piece_code = board[i][j]
                if piece_code == '':
                    color,piece_type = '',''
                else:
                    color = piece_code[0]
                    piece_type = piece_code[1]
                    square.occupied = True
                piece = Piece(color,piece_type,square)
                if piece_code == 'wk':
                    self.white_king = piece
                elif piece_code == 'bk':
                    self.black_king = piece
                square.piece = piece
                piece_row.append(piece)
            piece_arr.append(piece_row)
        self.squares = board_arr
        self.pieces = piece_arr
        self.white_capturables = set()
        self.black_capturables = set()
        self.white_moves = {}
        self.black_moves = {}
        self.white_castles = []
        self.black_castles = []
        self.check_for_white_castles = True
        self.check_for_black_castles = True
        self.history = None
    def white_king_coords(self):
        return self.white_king.square.get_coords()
    def black_king_coords(self):
        return self.black_king.square.get_coords()
    def get_square(self,coords):
        idx_1, idx_2 = coords
        return self.squares[idx_1][idx_2]
    def get_piece(self,coords):
        idx_1,idx_2 = coords
        return self.pieces[idx_1][idx_2]
    def remove_piece(self,coords):
        square = self.get_square(coords)
        square.occupied = False
        square.piece = Piece('','',square)
        self.pieces[coords[0]][coords[1]] = Piece('','',square)
    def force_move(self,orig_coords,new_coords):
        #Force a move even if it isn't valid
        new_square = self.get_square(new_coords)
        piece = self.get_piece(orig_coords)
        new_x,new_y = new_coords
        if new_coords not in piece.capturable:
            new_square.occupied = True
        if piece.piece == 'p' and (new_x == 0 or new_x == 7):
            piece.piece = 'q'
        new_square.piece = piece
        piece.square = new_square
        piece.has_moved = True
        self.pieces[new_x][new_y] = piece
        self.remove_piece(orig_coords)
    def move_piece(self,orig_coords,new_coords,turn):
        #Attempt to move a piece and raise an error if that move isn't possible
        new_square = self.get_square(new_coords)
        piece = self.get_piece(orig_coords)
        new_x,new_y = new_coords
        king_coords = self.white_king_coords() if turn == 'w' else self.black_king_coords()
        castle_coords = self.white_castles if turn == 'w' else self.black_castles
        king_castle_moves = []
        for king_move,_ in castle_coords:
            king_castle_moves.append(king_move)
        if new_coords in piece.moves:
            #If the new square doesn't have a piece there mark it as occupied
            if new_coords not in piece.capturable:
                new_square.occupied = True
            #Promotion
            if piece.piece == 'p' and (new_x == 0 or new_x == 7):
                piece.piece = 'q'
            #Update the new square
            new_square.piece = piece
            piece.square = new_square
            piece.has_moved = True
            #Update displayable pieces
            self.pieces[new_x][new_y] = piece
            #Remove the original location of the piece
            self.remove_piece(orig_coords)
        elif orig_coords == king_coords and new_coords in king_castle_moves:
            for king_move, rook_position in castle_coords:
                if king_move == new_coords:
                    rook = self.get_piece(rook_position)
                    if king_move[1] > rook_position[1]:
                        #Maybe make this smarter and more dynamic eventually
                        self.force_move(rook_position,rook.square.right.right.right.get_coords())
                        self.force_move(orig_coords,new_coords)
                    else:
                        self.force_move(rook_position,rook.square.left.left.get_coords())
                        self.force_move(orig_coords,new_coords)
        else:
            raise ValueError("Move not valid")
    def display(self):
        #Print the board to the console
        board = self.pieces
        letters = 'abcdefgh'
        board_str = ""

        # Add the column letters at the top
        board_str += "    " + "    ".join(letters) + "\n"
        board_str += "  " + "-" * 41 + "\n"

        # Add each row
        for i in range(len(board) - 1, -1, -1):
            row = f"{i + 1} |"  # Add the row number
            for j in range(len(board[i])):
                piece = board[i][j]
                piece_display = str(piece) if piece else " "  # Show piece or empty square
                row += f" {piece_display:^2} |"
            board_str += row + f" {i + 1}\n"  # Add row number again at the end
            board_str += "  " + "-" * 41 + "\n"

        # Add the column letters at the bottom
        board_str += "    " + "    ".join(letters) + "\n"

        # Print the board
        print(board_str)
    def update_all(self):
        self.black_capturables = set()
        self.white_capturables = set()
        self.black_moves = {}
        self.white_moves = {}
        #Update the entire board
        for row in self.pieces:
            for piece in row:
                #print(f'Updating {coords_to_str(piece.square.get_coords())}...')
                cpt, moves = piece.update_piece()
                if piece.color == 'b':
                    self.black_capturables.update(cpt)
                    self.black_moves[piece.square.get_coords()] = list(moves)
                elif piece.color == 'w':
                    self.white_capturables.update(cpt)
                    self.white_moves[piece.square.get_coords()] = list(moves)
    
    def turn(self,color):
        valid = False
        while not valid:
            inp = take_user_input()
            if type(inp) == tuple:
                _from, _to = inp
            else:
                if inp == 'undo' and self.history.history:
                    self.undo() #Call undo twice, because history is assigned right before the turn function is called
                    self.undo()
                    self.display()
                elif inp == 'undo' and not self.history.history:
                    print("There are no more moves to undo...Please add a valid move")
                    self.turn(color) #call itself recursively then return if no space
                return
            if self.get_piece(_from).color == "":
                print("There is no piece at that location")
                continue
            elif self.get_piece(_from).color != color:
                print("That piece is the wrong color")
                continue
            try:
                self.move_piece(_from,_to,color)
                valid = True
            except ValueError:
                print("That is not valid move. Please try again")
        self.display()
    def update_castles(self,turn):
        #Overwrite the possible castles
        if turn == 'w':
            self.white_castles = []
        else:
            self.black_castles = []

        #Find the rooks
        rooks = []
        for row in self.pieces:
            for piece in row:
                if piece.piece == 'r' and piece.color == turn:
                    rooks.append(piece)
        
        if len(rooks) == 0:
            return False #If there are no rooks you can't castle
        
        #Find the king
        king_coords = self.white_king_coords() if turn == 'w' else self.black_king_coords()
        king = self.get_piece(king_coords)
        
        #King Checks
        if king.has_moved or (all(rook.has_moved for rook in rooks)):
            return False
        if self.assess_check(turn):
            return 
        
        
        #Rook cheecks
        can_castle = False
        for rook in rooks:
            if rook.sees_king:
                rook_col = rook.square.get_coords()[1]
                attempting_board = copy.deepcopy(self)
                attempting_king = copy.deepcopy(king_coords)
                king_row, king_col = attempting_king

                # Track whether the king's path is clear
                path_clear = True

                # If king's column is greater than the rook's column, move left; otherwise, move right
                for _ in range(2):
                    if king_col > rook_col:
                        king_col -= 1
                    else:
                        king_col += 1

                    # Force the king move on the board copy
                    attempting_board.force_move(attempting_king, (king_row, king_col))
                    attempting_board.update_all()
                    
                    # Check if the king is in check
                    if attempting_board.assess_check(turn):
                        path_clear = False
                        break  # Stop checking further if the king's path is under attack
                    
                    # Update the king's current position
                    attempting_king = (king_row, king_col)

                # If the path is clear, the king can castle
                if path_clear:
                    castle_move = ((king_row, king_col),rook.square.get_coords())
                    if turn == 'w':
                        self.white_castles.append(castle_move)
                    else:
                        self.black_castles.append(castle_move)
    def assess_check(self,turn):
        if turn == 'w':
            return self.white_king_coords() in self.black_capturables
        else:
            return self.black_king_coords() in self.white_capturables
    def assess_checkmate(self,turn):
        temp_board = copy.deepcopy(self)
        if turn == 'w':
            #Look at the king's moves first, as most of the time the king can get himself out of check
            for move in self.white_moves[self.white_king_coords()]:
                piece_cord = self.white_king_coords()
                temp_board.move_piece(piece_cord,move,turn)
                temp_board.update_all()
                if not temp_board.assess_check(turn):
                    return False
                temp_board = copy.deepcopy(self)
            for piece_cord,move_list in self.white_moves.items():
                if piece_cord != self.white_king_coords():
                    for move in move_list:
                        #Try to move the new piece
                        temp_board.move_piece(piece_cord,move,turn)
                        temp_board.update_all() #THIS MIGHT BE SUPER SLOW WE'LL SEE
                        #See if the new position is in check. If it's possible to get out of check it's not checkmate
                        if not temp_board.assess_check(turn):
                            return False
                        temp_board = copy.deepcopy(self)
            #If no moves get out of check, then 
            return True
        else:
            #Look at the king's moves first, as most of the time the king can get himself out of check
            for move in self.black_moves[self.black_king_coords()]:
                piece_cord = self.black_king_coords()
                temp_board.move_piece(piece_cord,move,turn)
                temp_board.update_all()
                if not temp_board.assess_check(turn):
                    return False
                temp_board = copy.deepcopy(self)
            for piece_cord,move_list in self.white_moves.items():
                if piece_cord != self.black_king_coords():
                    for move in move_list:
                        #Try to move the new piece
                        temp_board.move_piece(piece_cord,move,turn)
                        temp_board.update_all() #THIS MIGHT BE SUPER SLOW WE'LL SEE
                        #See if the new position is in check. If it's possible to get out of check it's not checkmate
                        if not temp_board.assess_check(turn):
                            return False
                        temp_board = copy.deepcopy(self)
            #If no moves get out of check, then 
            return True
        
    def game_loop(self,turn):
        self.update_all() #MAYBE PLACE THIS SOMEWHERE ELSE
        long_turn = "White's" if turn == 'w' else "Black's"
        
        castle_status = self.check_for_white_castles if turn == 'w' else self.check_for_black_castles
        if castle_status:
            if self.update_castles(turn) is not None:
                castle_status = False
        #If checkmate without check, it's a stalemate
        if not self.assess_check(turn):
            if self.assess_checkmate(turn):
                print("STALEMATE! It's a draw.")
                return 'end'
            print(f"It's {long_turn} turn! Make a move.")
        else:
            if self.assess_checkmate(turn):
                long_name = "Black" if turn == 'w' else "White"
                print(f"CHECKMATE! {long_name} WINS!!")
                return 'end'
            print(f"It's {long_turn} turn! Be careful, you're in check!")
            
        board_copy = copy.deepcopy(self)#Copy the status of the board
        self.history = board_copy
        self.turn(turn)
    def undo(self):
        #Completely reassign the object
        if self.history:
            for attr, value in self.history.__dict__.items():
                setattr(self, attr, value)
    def play(self):
        print("Let's play chess!\nInitial Board State:")
        self.display()
        turn = 'w'
        while True:
            if self.game_loop(turn): #If this has a return, then the game is over!
                break
            #Invert the turn
            if turn == 'w':
                turn = 'b'
            else:
                turn = 'w'

board = Board()
board.play()
