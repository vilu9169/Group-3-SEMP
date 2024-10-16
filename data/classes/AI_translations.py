from data.classes.board import Board
from data.classes.piece import Piece
def board_translation(board):
    p1_color = ""
    for square in board.squares:
        board_converted = [[[],[],[],[]],
                           [[],[],[],[]],
                           [[],[],[],[]],
                           [[],[],[],[]]]
        for square in board.squares:
            board_converted[square.y][square.x] = square_translation(square, board.p1_color)
    return board_converted
        

def square_translation(square, p1_color):
    square_converted = [0]
    pieces = square.pieces
    if pieces:
        for piece in pieces:
            if piece.color == 'blue':
                if p1_color == 'blue':
                    square_converted.append(2)
                else:
                    square_converted.append(3)

            if piece.color == 'red':
                if p1_color == 'red':
                    square_converted.append(2)
                else:
                    square_converted.append(3)
            if piece.standing:
                square_converted[0] = 1
    return square_converted
            
def inverse_board_translation(board_AI_format, board):
    if board.p1_color == 'blue':
        p2_color = 'red'
    else:
        p2_color = 'blue'
    for y in range(4):
        for x in range(4):
            square = next((square for square in board.squares if square.x == x and square.y == y),None)
            standing = False
            
            if board_AI_format[y][x][0] == 1:
                standing = True
            for i in range(1, len(board_AI_format)):
                is_standing = False
                if i == len(board_AI_format) - 1 and standing:
                    is_standing = True
                if board_AI_format[i] == 2:
                    square.pieces.append(Piece((x,y),board.p1_color, board, is_standing))
                if board_AI_format[i] == 3:
                    square.pieces.append(Piece((x,y),p2_color, board, is_standing))