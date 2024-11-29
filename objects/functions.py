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
