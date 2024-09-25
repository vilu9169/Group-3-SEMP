import pygame

class Piece:
    def __init__(self, pos, color, board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.pieces = []
        self.standing = False
        img_path = 'data/imgs/' + color + '_standing.png' if self.standing else 'data/imgs/' + color + '_laying.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.square_width - 20, board.square_height - 20))




    #checks for valid moves
    #def valid_move(self):

    #moves the piece based on previous function
    #def move(self, pos):

    #returns whether the piece is standing or not
    #def is_standing(self)
