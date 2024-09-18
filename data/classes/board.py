class Board:
    def __init__(self, width, height):
        self.roundcount = 0
        self.width = width
        self.height = height
        self.tile_width = width // 4
        self.tile_height = height // 4
        self.piecesleft_b = 15
        self.piecesleft_r = 15
        self.selected_piece = None
        self.turn = 'player1'
        self.squares = self.create_squares()


    #generates squares for the board
    #def create_squares(self):

    #uses the square draw function to draw all squares on the pygame screen.
    #draw_board(self, screen):

    #returns the square on certain coordinates
    #def get_squares_from_pos(self,pos):

    #uses the above function to get the piece standing on a pos
    #def get_piece_from_pos(self,pos):

    #returns true if a player has reached the winning path
    #def get_path(self, color):

    #Returns true if it is a draw
    #def get_draw(self)

    #handles mouse clicks
    #def handle_click(self,mouse_x,mouse_y):

    #checks how many pieces a color has left
    #def pieces_left(self, color):

    #count how many pieces are on the board
    #def count_board_pieces(self):

    #places a piece based on color and mode. Also checks for start condition
    #def place(self, pos, color, standing)

    