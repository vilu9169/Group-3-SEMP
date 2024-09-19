import pygame

class Piece:
    def __init__(self, pos, color, board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.pieces = []
        self.standing = False



    #checks for valid moves
    #def valid_move(self):

    #moves the piece based on previous function
    #def move(self, pos):

    #returns whether the piece is standing or not
    #def is_standing(self)
