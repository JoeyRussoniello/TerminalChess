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
    map = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
    return f'{map[x]}{y + 1}'

class Square:
    def __init__(self,board,coords):
        self.left = None
        self.right = None
        self. up = None
        self.down = None
        self.occupied = False
        self.piece = None
        self.coords = coords
        self.board = board
    def get_coords(self):
        return self.coords
class Piece:
    def __init__(self,color,piece,square):
        if color.lower() not in ['b','w','']:
            raise ValueError("Color must be either 'b','w',or''")
        if piece.lower() not in ['k','q','r','b','n','p','']:
            raise ValueError("Piece must be in 'k','q','r','b','n','p',or''")
        self.color = color.lower()
        self.piece = 'pf' if piece.lower() == "p" else piece.lower()
        self.square = square
        self.moves = None
        self.capturable = None
    def __str__(self):
        white_pieces = {
            "k":'♔',
            'q':'♕',
            'r':'♖',
            'b':'♗',
            'n':'♘',
            'p':'♙',
            'pf':'♙',
        }
        black_pieces = {
            "k":'♚',
            'q':'♛',
            'r':'♜',
            'b':'♝',
            'n':'♞',
            'p':'♟',
            'pf':'♟',
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
        #Check left
        pointer = self.square
        while pointer.left:
            pointer = pointer.left
            self.moves.add(pointer.get_coords())
            if pointer.occupied:
                if assess_capturable(self,pointer.piece):
                    self.capturable.add(pointer.get_coords())
                else:
                    self.moves.remove(pointer.get_coords())
                break
        #Check right
        pointer = self.square
        while pointer.right:
            pointer = pointer.right
            self.moves.add(pointer.get_coords())
            if pointer.occupied:
                if assess_capturable(self,pointer.piece):
                    self.capturable.add(pointer.get_coords())
                else:
                    self.moves.remove(pointer.get_coords())
                break
        #Check down
        pointer = self.square
        while pointer.down:
            pointer = pointer.down
            self.moves.add(pointer.get_coords())
            if pointer.occupied:
                if assess_capturable(self,pointer.piece):
                    self.capturable.add(pointer.get_coords())
                else:
                    self.moves.remove(pointer.get_coords())
                break
        #Check up
        pointer = self.square
        while pointer.up:
            pointer = pointer.up
            self.moves.add(pointer.get_coords())
            if pointer.occupied:
                if assess_capturable(self,pointer.piece):
                    self.capturable.add(pointer.get_coords())
                else:
                    self.moves.remove(pointer.get_coords())
                break
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
        elif self.piece == 'pf':
            #On a pawn's first move, they are allowed to move twice
            self.pawn_update(first = True)
        elif self.piece == 'p':
            #On a pawn's second move, they are not allowed to move twice
            self.pawn_update(first = False)
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
                if piece_code == 'wk':
                    self.white_king_coords = (i,j)
                elif piece_code == 'bk':
                    self.black_king_coords = (i,j)
                piece = Piece(color,piece_type,square)
                square.piece = piece
                piece_row.append(piece)
            piece_arr.append(piece_row)
        self.squares = board_arr
        self.pieces = piece_arr
        self.white_capturables = set()
        self.black_capturables = set()
        self.white_moves = {}
        self.black_moves = {}
        self.history = None
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
    def move_piece(self,orig_coords,new_coords):
        new_square = self.get_square(new_coords)
        piece = self.get_piece(orig_coords)
        new_x,new_y = new_coords
        
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
            if piece.piece == 'pf':
                piece.piece = 'p' #Strip the first move labels from pawns if we move them
            #Update displayable pieces
            self.pieces[new_x][new_y] = piece
            #Remove the original location of the piece
            self.remove_piece(orig_coords)
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
                cpt, moves = piece.update_piece()
                if piece.color == 'b':
                    self.black_capturables.update(cpt)
                    self.black_moves[piece.square.get_coords()] = list(moves)
                    if piece.piece == 'k':
                        self.black_king_coords = piece.square.get_coords() 
                elif piece.color == 'w':
                    self.white_capturables.update(cpt)
                    self.white_moves[piece.square.get_coords()] = list(moves)
                    if piece.piece == 'k':
                        self.white_king_coords = piece.square.get_coords()
    
    def turn(self,color):
        valid = False
        while not valid:
            inp = take_user_input()
            if type(inp) == tuple:
                _from, _to = inp
            else:
                print("Undoing...")
                self.undo() #Call undo twice, because history is assigned right before the turn function is called
                self.undo()
                self.display()
                return
            if self.get_piece(_from).color == "":
                print("There is no piece at that location")
                continue
            elif self.get_piece(_from).color != color:
                print("That piece is the wrong color")
                continue
            try:
                self.move_piece(_from,_to)
                valid = True
            except ValueError:
                print("That is not valid move. Please try again")
        self.display()
    def assess_check(self,turn):
        if turn == 'w':
            return self.white_king_coords in self.black_capturables
        else:
            return self.black_king_coords in self.white_capturables
    
    def game_loop(self,turn):
        self.update_all() #MAYBE PLACE THIS SOMEWHERE ELSE
        long_turn = "White's" if turn == 'w' else "Black's"
        if not self.assess_check(turn):
            print(f"It's {long_turn} turn! Make a move.")
        else:
            print(f"It's {long_turn} turn! Be careful, you're in check!")
            
        board_copy = copy.deepcopy(self)#Copy the status of the board
        self.history = board_copy
        self.turn(turn)
    def undo(self):
        #Completely reassign the object
        if self.history:
            for attr, value in self.history.__dict__.items():
                setattr(self, attr, value)
    def play(self,numrounds = None):
        print("Let's play chess!\nInitial Board State:")
        self.display()
        turn = 'w'
        #Eventually change to dynamic determination of if the game is over
        if numrounds:
            for i in range(numrounds):
                self.game_loop(turn)
                #Invert the turn
                if turn == 'w':
                    turn = 'b'
                else:
                    turn = 'w'
        else:
            while True:
                self.game_loop(turn)
                #Invert the turn
                if turn == 'w':
                    turn = 'b'
                else:
                    turn = 'w'

board = Board()
board.play(numrounds=3)