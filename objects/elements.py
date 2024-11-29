from .functions import assess_capturable
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