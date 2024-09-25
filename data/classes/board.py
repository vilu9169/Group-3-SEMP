import pygame
from data.classes.square import Square
import pygame as pg
from data.classes.popup import show_popup
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
        rule_text = (
            "The game starts by player 1, either one of the two players sitting in front of the computer, "
            "choosing either red or blue as their piece color. Each player has 15 pieces of one’s color. "
            "The first two moves are special because each player places the other player's piece. After that, "
            "red plays red pieces and vice versa. As a player, you can either place or move pieces.\n\n"
            "Place: You can either place a piece flat or standing. Keep in mind that in order to make a line to win, "
            "the pieces have to be flat. You can place a piece either on an empty square or on any flat piece.\n\n"
            "Move: You can move a piece or a stack if the piece/bottom piece is your color. One cannot move a piece/stack "
            "diagonally. When moving a stack, one piece from the bottom is left on a square/flat piece for every step. "
            "Keep in mind that you can only move a stack as long as the bottom piece is your color. It is not possible to "
            "switch direction when moving a stack.\n\n"
            "To win the game, either player has to form a path from one side of the board to the opposite with pieces of their "
            "own color. Once again, the pieces have to be flat in order to win. If no moves are available, the one with the most "
            "flat pieces on top wins. If equal, the game ends in a draw."
        )
        show_popup(screen, rule_text)




    #returns the square on certain coordinates
    

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
    
    #count how many pieces are on the board in a draw
    #def count_board_pieces(self):


    def get_square_from_coord(self, coord):
        for square in self.squares:
            if square.pos == coord:
                return square
            
    def get_piece_from_pos(self, coord):
        square = self.get_square_from_coord(coord)
        return square.occupying_piece
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
    
    def populate(self, coord,screen):
        square = self.get_square_from_coord(coord)
        piece = self.get_piece_from_pos(coord)
        print(self.color)
        self.color = "blue" if self.turn == "player1" else "red"
        if square.is_valid_coordinate(coord) and piece is None:
            print("inside populate")
            square.occupying_piece  = Piece(coord, self.color, self)
            print(square.occupying_piece)
            square.draw_square(screen)

    def draw_valid(self, moves, screen):
        color = (0, 0, 0)  # Black circles to mark valid moves
        for move in moves:
            print("Inside draw_valid, drawing circle for move")
            # Convert grid position (square.x, square.y) to pixel position
            circle_x = move.abs_x + self.square_width // 2
            circle_y = move.abs_y + self.square_height // 2
            print(f"Drawing at pixel: ({circle_x}, {circle_y})")
            pygame.draw.circle(screen, color, (circle_x, circle_y), self.square_width // 2, 5)
            pygame.display.flip()

    def handle_click(self, event, mouse_x, mouse_y, action, screen):
        print("inside handle_click")
        self.draw_board(screen)
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left mouse button
            square = self.get_square_from_pos(event.pos)
            if square is not None:
                if action == action.MOVE:
                    if self.selected_piece is None:  # Selecting a piece to move
                        if square.occupying_piece is not None and square.occupying_piece.color == self.color:
                            print(f"Selected piece at {square.x, square.y}")
                            self.selected_piece = square
                            valid_moves = self.valid_move(square)
                            self.draw_valid(valid_moves, screen)  # Highlight valid moves
                    else:  # Moving the selected piece
                        if self.move(self.selected_piece, square, screen):
                            self.selected_piece = None  # Reset the selected piece after moving
                        
                elif action == action.PLACE:
                    if self.populate(square.pos, screen):
                        if self.turn == "player1":
                            self.turn = "player2"
                        else:
                            self.turn = "player1"
                        self.selected_piece = None  # Reset selection after placing
                    else:
                        print("Invalid placement")


                

    #checks how many pieces a color has left. From the beginning 15 of each color. When one i place, the amount is reduced by one.
    def pieces_left(self, color):   
        if color == "blue":
            self.piecesleft_blue -= 1
            return self.piecesleft_blue
        else:
            self.piecesleft_red -= 1
            return self.piecesleft_red

    def valid_square(self, square):
        if square.occupying_piece is None:
            return True
        if square.occupying_piece.standing:
            return False
        return True
    # places a piece based on color and mode. Also checks for start condition
     #checks for valid moves
    def valid_move(self, square):
        valid = []
        if square.occupying_piece is None or square.occupying_piece.standing:
            print('invalid piece')
            return None
        for neighbour in square.neighbours():
                    x, y = neighbour
                    for square in self.squares:
                        if square.x == x and square.y == y:
                            if self.valid_square(square):
                                valid.append(square)
        return valid


    def move(self, start_square, end_square, screen):
        # Check if the move is valid
        if end_square in self.valid_move(start_square):
            # Move the piece
            print(f"Moving piece from {start_square.x, start_square.y} to {end_square.x, end_square.y}")
            end_square.occupying_piece = start_square.occupying_piece  # Move the piece to the new square
            start_square.occupying_piece = None  # Clear the starting square
            
            # Redraw the updated board and pieces
            self.draw_board(screen)

            # Change the turn after the move
            if self.turn == "player1":
                self.turn = "player2"
            else:
                self.turn = "player1"
            
            return True  # Indicate the move was successful
        else:
            print("Invalid move")
            return False

    def place(self, pos, color, standing):

        #MOUSECLICK
        #CALL VALIDMOVE FUNCTION
        #IF TRUE PLACE, ELSE ERROR MESSAGE AND USER GETS TO TRY AGAIN

        print("place new piece")
