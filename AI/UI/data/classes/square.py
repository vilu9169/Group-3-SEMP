import pygame
player1 = 2
player2 = 3

class Square:
    def __init__(self, x, y, width, height):
        self.x = x #row
        self.y = y #column
        self.width = width 
        self.height = height
        self.abs_x = x * width + 200 #row in width, center offset
        self.abs_y = y * height + 100 #column in height, centter offset
        self.abs_pos = (self.abs_x, self.abs_y) #position of tile
        self.pos = (x, y) #coordinates
        self.color = (255,255,255)
        self.pieces = []
        self.occupying_piece = None 
        self.bottom_piece = None 
        self.highlight = False
        # self.coord = self.get_coord()
        self.rect = pygame.Rect( #used for drawing on screen
            self.abs_x,
            self.abs_y,
            self.width,
            self.height
        )


    def get_pieces(self, player_1_color):
        pieces = []
        for piece in self.pieces:
            if player_1_color == "blue":
                if piece.color == "blue":
                    pieces.append(player1)
                else:
                    pieces.append(player2)
            else:
                if piece.color == "blue":
                    pieces.append(player2)
                else:
                    pieces.append(player1)
            if piece.standing == 1:
                pieces.insert(0,1)
                return pieces

        pieces.insert(0,0)
        return pieces

    def get_coord(self):
        """returns the coordinates of the square
        Param: the square to get coordinates for
        returns: Coordinates for given square on the format (x, y)"""
        return(self.x, self.y)

    def draw_square(self,screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)
        if self.occupying_piece != None:
            if self.pieces:
                offset = 0;
                for piece in self.pieces:
                    centering_rect = piece.img.get_rect()
                    centering_rect.center = self.rect.center
                    if piece.standing:
                        offset += 17
                    screen.blit(piece.img, (centering_rect[0],centering_rect[1] + offset))
                    offset -= 20

        if self.highlight:
            color = (0, 0, 0)
            circle_x = self.abs_x + self.width // 2
            circle_y = self.abs_y + self.height // 2
            pygame.draw.circle(screen, color, (circle_x, circle_y), self.width // 2, 5)


    def all_squares_between(self, square2, board):
        squares =[]
        if self.x == square2.x:
            step = 1 if self.y < square2.y else -1
            for y in range(self.y+step, square2.y , step):
                squares.append(board.get_square_from_coord((self.x, y)))

        if self.y == square2.y:
            step = 1 if self.x < square2.x else -1
            for x in range(self.x+step, square2.x , step):
                squares.append(board.get_square_from_coord((self.y, x)))

        return squares
 

    def neighbours(self):###TODO ADD LOGIC FOR COLOR CHECK ON NEIGHBOURS
        """returns the ajdacent neighbours coordinates.
        Param: Square that neighbours will be generated from 
        returns: a list with all the neighbours from given square"""
        neighbours_coords = [
            ((self.x - 1, self.y),0),   # left
            ((self.x + 1, self.y), 1),   # right
            ((self.x, self.y - 1), 2),   # up
            ((self.x, self.y + 1), 3)    # down
        ]

        valid_neighbours = [coord for coord in neighbours_coords if self.is_valid_coordinate(coord[0])]
        return valid_neighbours
    
    def stack_neighbours(self):
        neighbours_coords = []
        for i in range(1,4):
            neighbours_coords.append(((self.x - i, self.y), 0))
            neighbours_coords.append(((self.x + i, self.y),1))
            neighbours_coords.append(((self.x, self.y - i), 2))
            neighbours_coords.append(((self.x, self.y + i), 3))
        valid_neighbours = [coord for coord in neighbours_coords if self.is_valid_coordinate(coord[0])]
        return valid_neighbours
    
            
    def is_valid_coordinate(self, coord):
        """Checks if a coordinate is within the 4x4 grid (could be useful)
        Param: neighbour to be checked
        returns: boolean (True/False) depending on if the neighbour is within the grid or not"""
        x, y = coord
        return 0 <= x < 4 and 0 <= y < 4
    
    def valid_square(self):
        if self.occupying_piece is None:
            return True
        if self.occupying_piece.standing:
            return False
        return True
    


        

            

