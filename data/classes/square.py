import pygame

class Square:
    def __init__(self, x, y, width, height):
        self.x = x #row
        self.y = y #column
        self.width = width 
        self.height = height
        self.abs_x = x * width #row in width
        self.abs_y = y * height #column in height
        self.abs_pos = (self.abs_x, self.abs_y) #position of tile
        self.pos = (x, y) #coordinates
        self.color = (220, 208, 194) 
        self.occupying_piece = None
        self.coord = self.get_coord()
        self.rect = pygame.Rect( #used for drawing on screen
            self.abs_x,
            self.abs_y,
            self.width,
            self.height
        )
#returns the coordinates of the square
#def get_coord(self)

#draws the square on a pygame screen using rect.
#def draw_square(self,screen)

#returns the ajdacent neighbours coordinates. 
#def neighbours(self)