import pygame
from data.classes.square import Square
from data.classes.gamestate import GameState
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
        self.color = ""
        self.squares = self.create_squares()
        self.pieceonboard_blue = 0
        self.pieceonboard_red = 0
        self.action = None


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
    
    def populate(self, coord, does_stand):
        square = self.get_square_from_coord(coord)
        piece = self.get_piece_from_pos(coord)
        if square.is_valid_coordinate(coord) and piece is None:
            if self.piecesleft_blue == 15 or self.piecesleft_red == 15:
                self.color = "blue" if self.color == "red" else "red"
            square.occupying_piece  = Piece(coord, self.color, self, does_stand)
            if self.color == "blue":
                self.piecesleft_blue -=1
                if self.piecesleft_blue == 14:
                    self.color = "red"
            elif self.color == "red":
                self.piecesleft_red -=1
                if self.piecesleft_red == 14:
                    self.color = "blue"
            else:
                print("knas med färger")
            return True
        
        elif square.is_valid_coordinate(coord) and piece is not None:
            placed_piece = self.get_piece_from_pos(coord)
            piece_standing = placed_piece.standing
            if(piece_standing):
                print("Stack is not avaliable!")
                return False
            else:
                print("Yeah you can stack here")
                return True
            
        return False;

    def new_turn(self):
        self.check_win()
        self.selected_piece = None  # Reset the selected piece after moving
        self.color = "blue" if self.color == "red" else "red"
        self.turn = "player1" if self.turn == "player2" else "player2"
        self.action = None
        return True;
        
        

    def handle_click(self, event):
        if self.action is None:
            return;
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left mouse button
            square = self.get_square_from_pos(event.pos)
            if square is not None:
                does_stand = False
                if self.action == GameState.MOVE:
                    if self.selected_piece is None:  # Selecting a piece to move
                        if square.occupying_piece is not None and square.occupying_piece.color == self.color:
                            self.selected_piece = square.occupying_piece
                            self.selected_piece.valid_move(self)
                            self.check_win()
                            # self.draw_valid(valid_moves, screen)  # Highlight valid moves
                    elif self.selected_piece.move(square, self):
                            self.new_turn()

                elif self.action == GameState.PLACE and self.show_pieces_left(self.color) > 0:
                    if self.populate(square.pos, does_stand):
                        self.new_turn()
                    else:
                        print("Invalid placement")
                        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:  # Left mouse button
            square = self.get_square_from_pos(event.pos)
            if square is not None:
                does_stand = True
            if self.action == GameState.PLACE and self.show_pieces_left(self.color) > 0:
                if self.populate(square.pos, does_stand):
                    self.pieces_left(self.color)
                    self.new_turn()
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

    def show_pieces_left(self, color):
        if color == "blue":
            return self.piecesleft_blue
        else:
            return self.piecesleft_red

    def place(self, pos, color, standing):

        #MOUSECLICK
        #CALL VALIDMOVE FUNCTION
        #IF TRUE PLACE, ELSE ERROR MESSAGE AND USER GETS TO TRY AGAIN

        print("place new piece")

    def check_win(self):
        top_row = self.squares[0:4]
        for square in top_row:
            if self.check_path(square, []):
                print("WIN")
                

    def check_path(self, square, visited_squares):##ALWAYS START FROM THE TOP ROW
        if square.occupying_piece is None:
            return False
        visited_squares.append(square)
        neighbors = square.neighbours()
        for neighbor in neighbors:
            neighbor = self.get_square_from_coord(neighbor)
            #print(neighbor)
            if neighbor.occupying_piece is not None and not neighbor.occupying_piece.standing and neighbor.occupying_piece.color == self.color and visited_squares.count(neighbor) == 0:
                visited_squares.append(neighbor)
                self.check_path(neighbor, visited_squares=visited_squares)

                if neighbor.y == 3:
                    print("WIN")
                    print(self.color)
                    return True
        
        return False
