from data.classes.board import Board
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
            
    