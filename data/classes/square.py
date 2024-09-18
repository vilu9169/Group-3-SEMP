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
        self.occupying_piece = None
        # self.coord = self.get_coord()
        self.rect = pygame.Rect( #used for drawing on screen
            self.abs_x,
            self.abs_y,
            self.width,
            self.height
        )
#returns the coordinates of the square
#def get_coord(self)

    def draw_square(self,screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)

#returns the ajdacent neighbours coordinates. 
#def neighbours(self)
