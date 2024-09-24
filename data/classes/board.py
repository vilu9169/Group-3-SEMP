# /* Board.py

import pygame
from data.classes.square import Square
# Game state checker
class Board:
    def __init__(self, width, height, tiles):
        self.width = width
        self.height = height
        self.tile_width = width // tiles
        self.tile_height = height // tiles
        self.selected_piece = None
        self.turn = 'white'
        self.config = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', '']
        ]
        
        self.squares = self.generate_squares()

    def generate_squares(self):
        output = []
        for y in range(8):
            for x in range(8):
                output.append(
                    Square(x,  y, self.tile_width, self.tile_height)
                )
        return output

    def get_square_from_pos(self, pos):
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square

    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece
    
    def draw(self, display):
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True
        for square in self.squares:
            square.draw(display)

    def get_tile_size(self):
        return (self.tile_width, self.tile_height)