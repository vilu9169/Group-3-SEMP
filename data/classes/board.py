import pygame
from data.classes.square import Square
from data.classes.piece import Piece
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
        
    #returns the square on certain coordinates
    def get_square_from_coord(self, coord):
        for square in self.squares:
            if square.pos == coord:
                return square
        
    # uses the above function to get the piece standing on a pos
    def get_piece_from_pos(self, coord):
        square = self.get_square_from_pos(coord)
        return square.occupying_piece

    def populate(self, coord,screen):
        square = self.get_square_from_coord(coord);
        piece = self.get_piece_from_pos(coord);
        print(self.color)
        if square.is_valid_coordinate(coord) and piece is None:
            square.occupying_piece  = Piece(coord, self.color, self)
            square.draw_square(screen)




    #returns true if a player has reached the winning path
    #def get_path(self, color):

    #Returns true if it is a draw
    #def get_draw(self)

    #count how many pieces are on the board in a draw
    #def count_board_pieces(self):

    #handles mouse clicks
    """param: Position in pixels
        Returns: Square"""
    def get_square_from_pos(self, pos):
        x, y = pos
        square_x = x // self.square_width - 2 # Dont know why but hardcode 2 works
        square_y = y // self.square_height - 1  # Dont know why but hardcode 1 works
        for square in self.squares:
            if square.x == square_x and square.y == square_y:
                return square
        return None
        
    def handle_click(self,event, mouse_x, mouse_y):
        print("inside handle_click")
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                square = self.get_square_from_pos(event.pos)
                if square is not None:
                    print(f"Mouse clicked at {event.pos}")
                    print(f"Mouse clicked at square: {square.x, square.y}")


                

    #checks how many pieces a color has left
    #def pieces_left(self, color):

    def valid_square(self, square):
        pass
    #places a piece based on color and mode. Also checks for start condition
    #def place(self, pos, color, standing)
    def place(self, pos, color, standing):
        #MOUSECLICK
        #CALL VALIDMOVE FUNCTION
        #IF TRUE PLACE, ELSE ERROR MESSAGE AND USER GETS TO TRY AGAIN

        print("place new piece")
