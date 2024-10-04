import pygame

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
        self.occupying_piece = None if not self.pieces else self.pieces[-1]
        self.bottom_piece = None if not self.pieces else self.pieces[0]
        self.highlight = False
        # self.coord = self.get_coord()
        self.rect = pygame.Rect( #used for drawing on screen
            self.abs_x,
            self.abs_y,
            self.width,
            self.height
        )


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
            else:
                "Needed until stack movement has been fixed"
                centering_rect = self.occupying_piece.img.get_rect()
                centering_rect.center = self.rect.center
                screen.blit(self.occupying_piece.img, centering_rect.topleft)
        if self.highlight:
            color = (0, 0, 0)
            circle_x = self.abs_x + self.width // 2
            circle_y = self.abs_y + self.height // 2
            pygame.draw.circle(screen, color, (circle_x, circle_y), self.width // 2, 5)



 

    def neighbours(self):###TODO ADD LOGIC FOR COLOR CHECK ON NEIGHBOURS
        """returns the ajdacent neighbours coordinates.
        Param: Square that neighbours will be generated from 
        returns: a list with all the neighbours from given square"""
        neighbours_coords = [
            (self.x - 1, self.y),   # Up
            (self.x + 1, self.y),   # Down
            (self.x, self.y - 1),   # Left
            (self.x, self.y + 1)    # Right
        ]

        valid_neighbours = [coord for coord in neighbours_coords if self.is_valid_coordinate(coord)]
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
    


        

            

