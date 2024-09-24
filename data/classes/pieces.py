import pygame

from data.classes.board import Board

class Piece:
    def __init__(self, pos, color, board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.has_moved = False

    def get_moves(self, board):
        output = []
        for direction in self.get_possible_moves(board):
            for square in direction:
                if square.occupying_piece is not None:
                    if square.occupying_piece.color == self.color:
                        break
                    else:
                        output.append(square)
                        break
                else:
                    output.append(square)
        return output
    
    def draw_flat_stone(self, x, y, board, screen):
        center = (x * board.get_tile_size()[0] + board.get_tile_size()[0] // 2, y * board.get_tile_size()[1] + board.get_tile_size()[1] // 2)
        pygame.draw.circle(screen, self.color, center, board.get_tile_size()[0] // 3)