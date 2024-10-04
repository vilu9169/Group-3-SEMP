import pygame

class Piece:
    def __init__(self, pos, color, board, does_stand):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.standing = does_stand
        img_path = 'data/imgs/' + color + '_standing.png' if self.standing else 'data/imgs/' + color + '_laying.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.square_width - 20, board.square_height - 20))



    def move(self, square, board):
        # Check if the move is valid

        print(square.pos)
        if square in self.valid:
            # Move the piece
            prev_square = board.get_square_from_coord(self.pos)
            square.occupying_piece = self  # Move the piece to the new square
            self.pos = square.pos
            self.x = square.x
            self.y = square.y
            prev_square.occupying_piece = None  # Clear the starting square
            
            # Redraw the updated board and pieces

            for squares in board.squares:
              squares.highlight = False
            self.valid = []
            return True  # Indicate the move was successful
        else:
            print("Invalid move")
            return False
        
    def valid_move(self,board):
        valid = []
        if self is None or self.standing:
            print('invalid piece')
            return None
        selected_square = board.get_square_from_coord(self.pos)

        for neighbour in selected_square.neighbours():
                    x, y = neighbour
                    for square in board.squares:
                        if square.x == x and square.y == y:
                            if square.valid_square():
                                valid.append(square)
                                square.highlight = True
        self.valid = valid

        

    
    #moves the piece based on previous function
    #def move(self, pos):

    #returns whether the piece is standing or not
    def is_standing(self):
        return self.standing
