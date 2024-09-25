from data.classes.square import Square
import pygame as pg
from data.classes.popup import show_popup

class Board:
    def __init__(self, width, height):
        self.roundcount = 0
        self.width = width
        self.height = height
        self.square_width = width // 4
        self.square_height = height // 4
        self.piecesleft_blue = 15
        self.piecesleft_red = 15
        self.selected_piece = None
        self.turn = "player1"
        self.color = " "
        self.squares = self.create_squares()
        self.pieceonboard_blue = 0
        self.pieceonboard_red = 0


    #generates squares for the board
    def create_squares(self):
        squares = []
        for y in range(4):
            for x in range(4):
                square = Square(x, y, self.square_width, self.square_height)
                squares.append(square)
        return squares


    #uses the square draw function to draw all squares on the pygame screen.
    def draw_board(self, screen):
        for square in self.squares:
            square.draw_square(screen)

    def whose_turn(self):
        if self.turn == "player1":
            return "Player 1\'s turn"
        else:
            return "Player 2\'s turn"
        
    #return a pop up with rules
    def pop_up_rules(self, screen):
        print("Rules är påväg")
        show_popup(screen, "Rules")




    #returns the square on certain coordinates
    #def get_squares_from_pos(self, pos):

    #uses the above function to get the piece standing on a pos
    #def get_piece_from_pos(self, pos):

    #returns true if a player has reached the winning path
    #def get_path(self, color):

    #Returns true if it is a draw
    #def get_draw(self)

    #count how many pieces are on the board of each color in case of a draw
    def count_board_pieces(self):
        for square in self.squares:
            if square.piece == "blue":
                self.pieceonboard_blue += 1
            elif square.piece == "red":
                self.pieceonboard_red += 1
    
    #handles mouse clicks
    #def handle_click(self, mouse_x, mouse_y):

    #checks how many pieces a color has left. From the beginning 15 of each color. When one i place, the amount is reduced by one.
    def pieces_left(self, color):   
        if color == "blue":
            self.piecesleft_blue -= 1
            return self.piecesleft_blue
        else:
            self.piecesleft_red -= 1
            return self.piecesleft_red

      

    #places a piece based on color and mode. Also checks for start condition
    #def place(self, pos, color, standing)
    def place(self, pos, color, standning):
        print("place new piece")
