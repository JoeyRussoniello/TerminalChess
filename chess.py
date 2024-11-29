import copy #Allows the object to be copied for history

def translate_input(input):
    col, row = input
    row = int(row) - 1
    col = ord(col) - ord('a')
    coords = (row,col)
    return coords

def take_user_input():
    valid = False
    while not valid:
        _from = input("What piece would you like to move? (Type 'undo' to go back a move)")
        if _from == "undo":
            return 'undo'
        if len(_from) != 2:
            print("Input must be in the form a-h0-8 Ex:a1. Try again")
            continue
        letter = _from[0]
        num = _from[1]
        if letter not in 'abcdefgh' or num not in '12345678':
            print("Input must be in the form a-h0-8 Ex:a1. Try again")
            continue
        _from = translate_input(_from)
        valid = True
    valid = False
    while not valid:
        _to = input("Where would like you to move it?")
        if len(_to) != 2:
            print("Input must be in the form a-h0-8 Ex:a1. Try again")
            continue
        letter = _to[0]
        num = _to[1]
        if len(_from) < 2 or letter not in 'abcdefgh' or num not in '12345678':
            print("Input must be in the form a-h0-8 Ex:a1. Try again")
            continue
        _to = translate_input(_to)
        valid = True
    return (_from,_to)

def assess_capturable(piece,other_piece):
    piece_color = piece.color
    other_piece_color = other_piece.color
    return piece_color != other_piece_color

def coords_to_str(coords):
    x,y = coords
    map = {
        0:'a',
        1:'b',
        2:'c',
        3:'d',
        4:'e',
        5:'f',
        6:'g',
        7:'h'
    }
    return f'{map[x]}{y + 1}'

class Square:
    def __init__(self,board,coords):
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.occupied = False
        self.piece = None
        self.coords = coords
        self.board = board
    def get_coords(self):
        return self.coords
    def is_under_attack(self, moves):
        for move_arr in moves.iems():
            for move in move_arr:
                if move == self.get_coords():
                    return True
        return False
class Piece:
    def __init__(self,color,piece,square):
        if color.lower() not in ['b','w','']:
            raise ValueError("Color must be either 'b','w',or''")
        if piece.lower() not in ['k','q','r','b','n','p','']:
            raise ValueError("Piece must be in 'k','q','r','b','n','p',or''")
        self.color = color.lower()
        self.piece = piece.lower()
        self.has_moved = False
        self.square = square
        self.moves = None
        self.capturable = None
        self.sees_king = None #Only used for rooks to determine if castling is possible
    def __str__(self):
        white_pieces = {
            "k":'♔',
            'q':'♕',
            'r':'♖',
            'b':'♗',
            'n':'♘',
            'p':'♙',
        }
        black_pieces = {
            "k":'♚',
            'q':'♛',
            'r':'♜',
            'b':'♝',
            'n':'♞',
            'p':'♟',
        }
        if self.color == 'w':
            return white_pieces[self.piece]
        elif self.color == 'b':
            return black_pieces[self.piece]
        else:
            return f''
    def __format__(self,fmt):               
        return f'{str(self):{fmt}}'
    def rook_update(self):
        def traverse_and_update(direction_func):
            pointer = self.square
            has_seen_king = False #Keep track of whether a king has ever been seen
            while direction_func(pointer):
                pointer = direction_func(pointer)
                self.moves.add(pointer.get_coords())
                if pointer.occupied:
                    if pointer.piece.piece == 'k' and pointer.piece.color == self.color: #IF we see our king, remember that
                        has_seen_king = True 
                    if assess_capturable(self, pointer.piece):
                        self.capturable.add(pointer.get_coords())
                    else:
                        self.moves.remove(pointer.get_coords())
                    break
            return has_seen_king

        # Define direction functions
        directions = [lambda p: p.left, lambda p: p.right, lambda p: p.up, lambda p: p.down]

        #Reset king sight before traversal
        self.sees_king = False
        # Traverse in all directions
        for direction in directions:
            if traverse_and_update(direction): #If the king was seen during iteration, update that in the Piece's memory
                self.sees_king = True

    def bishop_update(self):
        #Check leftup
        pointer = self.square
        while pointer.left and pointer.up:
            pointer = pointer.left.up
            self.moves.add(pointer.get_coords())
            if pointer.occupied:
                if assess_capturable(self,pointer.piece):
                    self.capturable.add(pointer.get_coords())
                else:
                    self.moves.remove(pointer.get_coords())
                break
        #Check rightup
        pointer = self.square
        while pointer.right and pointer.up:
            pointer = pointer.right.up
            self.moves.add(pointer.get_coords())
            if pointer.occupied:
                if assess_capturable(self,pointer.piece):
                    self.capturable.add(pointer.get_coords())
                else:
                    self.moves.remove(pointer.get_coords())
                break
        #Check leftdown
        pointer = self.square
        while pointer.left and pointer.down:
            pointer = pointer.left.down
            self.moves.add(pointer.get_coords())
            if pointer.occupied:
                if assess_capturable(self,pointer.piece):
                    self.capturable.add(pointer.get_coords())
                else:
                    self.moves.remove(pointer.get_coords())
                break
        #Check rightdown
        pointer = self.square
        while pointer.right and pointer.down:
            pointer = pointer.right.down
            self.moves.add(pointer.get_coords())
            if pointer.occupied:
                if assess_capturable(self,pointer.piece):
                    self.capturable.add(pointer.get_coords())
                else:
                    self.moves.remove(pointer.get_coords())
                break
    def knight_update(self):
        # Define all possible knight moves relative to the current position
        pointer = self.square
        if pointer.up and pointer.up.up:
            pointer = pointer.up.up
            self.moves.add(pointer.left.get_coords()) if pointer.left else ()
            self.moves.add(pointer.right.get_coords()) if pointer.right else()
        
        pointer = self.square
        if pointer.down and pointer.down.down:
            pointer = pointer.down.down
            self.moves.add(pointer.left.get_coords()) if pointer.left else ()
            self.moves.add(pointer.right.get_coords()) if pointer.right else ()

        pointer = self.square
        if pointer.left and pointer.left.left:
            pointer = pointer.left.left
            self.moves.add(pointer.up.get_coords()) if pointer.up else ()
            self.moves.add(pointer.down.get_coords()) if pointer.down else ()

        pointer = self.square
        if pointer.right and pointer.right.right:
            pointer = pointer.right.right
            self.moves.add(pointer.up.get_coords()) if pointer.up else ()
            self.moves.add(pointer.down.get_coords()) if pointer.down else ()
        
        for move in list(self.moves).copy():
            other_square = self.square.board.get_square(move)
            if other_square.occupied:
                if assess_capturable(self,other_square.piece):
                    self.capturable.add(other_square.get_coords())
                else:
                    self.moves.remove(other_square.get_coords())
    def pawn_update(self, first = False):
        #Add valid movdes, first_move, en_passant
        pointer = self.square
        if self.color == 'w':
            if pointer.down:
                pointer = pointer.down
                if not pointer.occupied:
                    self.moves.add(pointer.get_coords())
                    #If first move, repeat this
                    if first and pointer.down:
                        pointer = pointer.down
                        if not pointer.occupied:
                            self.moves.add(pointer.get_coords())
        else:
            if pointer.up:
                pointer = pointer.up
                if not pointer.occupied:
                    self.moves.add(pointer.get_coords())
                    #If first move, repeat this
                    if first and pointer.up:
                        pointer = pointer.up
                        if not pointer.occupied:
                            self.moves.add(pointer.get_coords())
        #Caputrable pieces ondiagonals
        if self.color == 'w':
            if self.square.right:
                pointer = self.square.down.right
                if pointer.occupied and assess_capturable(self,pointer.piece):
                    self.moves.add(pointer.get_coords())
                    self.capturable.add(pointer.get_coords())
            
            if self.square.left:
                pointer = self.square.down.left
                if pointer.occupied and assess_capturable(self,pointer.piece):
                    self.moves.add(pointer.get_coords())
                    self.capturable.add(pointer.get_coords())
        else:
            if self.square.right:
                pointer = self.square.up.right
                if pointer.occupied and assess_capturable(self,pointer.piece):
                    self.moves.add(pointer.get_coords())
                    self.capturable.add(pointer.get_coords())
            if self.square.left:
                pointer = self.square.up.left
                if pointer.occupied and assess_capturable(self,pointer.piece):
                    self.moves.add(pointer.get_coords())
                    self.capturable.add(pointer.get_coords())
    def queen_update(self):
        self.rook_update()
        self.bishop_update()
    def king_update(self):
        x, y = self.square.coords
        updates = [-1, 0, 1]  # Possible changes for x and y
        
        for update_x in updates:
            for update_y in updates:
                # Skip the case where both update_x and update_y are 0 (no movement)
                if update_x == 0 and update_y == 0:
                    continue
                
                updated_x = x + update_x
                updated_y = y + update_y
                
                # Ensure the move stays within board bounds
                if 0 <= updated_x <= 7 and 0 <= updated_y <= 7:
                    target_square = self.square.board.get_square((updated_x, updated_y))  # returns the square at (x, y)
                    # If the target square is valid, add it to moves and check for capturability
                    if target_square:
                        self.moves.add(target_square.get_coords())
                        if target_square.occupied:
                            if assess_capturable(self, target_square.piece):
                                self.capturable.add(target_square.get_coords())
                            else:
                                self.moves.remove(target_square.get_coords())
    def update_piece(self):
        self.moves = set()
        self.capturable = set()
        
        if self.piece == 'r':
            self.rook_update()
        elif self.piece == 'b':
            self.bishop_update()
        elif self.piece == 'q':
            self.queen_update()
        elif self.piece == 'n':
            self.knight_update()
        elif self.piece == 'p':
            #On a pawn's second move, they are not allowed to move twice
            self.pawn_update(first = not self.has_moved)
        elif self.piece == "k":
            self.king_update()
        
        return (self.capturable,self.moves)
    def display_info(self):
        print(f'Piece: {self.piece} or {str(self)}')
        print(f'Capturable Pieces: {self.capturable}')
        print(f'Valid Moves: {self.moves}')
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
        board_str = ""
        final_row = ""
        letters = 'abcdefgh'
        for i in range(len(board)-1,-1,-1):
            row = ""
            if i == 0:
                final_row += ' '+f'{letters[i]:^5}'
            else:
                final_row += f'{letters[i]:^4}'
            for j in range(len(board[i])):
                if j == 0:
                    row += " "+"-"*33+"\n"+str(i+1)+f"|{board[i][j]:^3}|"
                else:
                    row += f"{board[i][j]:^3}|"
                
            board_str+= row + "\n" 
        final_row = final_row[::-1]
        print(board_str + final_row)
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
            for piece_cord,move_list in self.white_moves.items():
                for move in move_list:
                    #print(f"Looking at {coords_to_str(piece_cord)}-{coords_to_str(move)}")
                    #Try to move the new piece
                    temp_board.move_piece(piece_cord,move,turn)
                    temp_board.update_all() #THIS MIGHT BE SUPER SLOW WE'LL SEE
                    #See if the new position is in check. If it's possible to get out of check it's not checkmate
                    if not temp_board.assess_check('w'):
                        return False
                    temp_board = copy.deepcopy(self)
            #If no moves get out of check, then 
            return True
        else:
            for piece_cord,move_list in self.black_moves.items():
                for move in move_list:
                    #Try to move the new piece, and update lines of sight
                    temp_board.move_piece(piece_cord,move,turn)
                    temp_board.update_all()
                    #See if the new position is in check
                    if not temp_board.assess_check('b'):
                        return False
                    temp_board = copy.deepcopy(self)
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