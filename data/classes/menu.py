import pygame as pg
from enum import Enum

class GameState(Enum):
    RED = -1
    TITLE = 0
    BLUE = 1

class Butt():

    def __init__(self, position, width, height, color, action = None):

        self.mouse_over = False  
        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self.action = action

        self.normal_rect = pg.Rect( 
            self.position[0],
            self.position[1],
            self.width,
            self.height
        )
        
        self.highlighted_rect = pg.Rect( 
            self.position[0] -(width*0.1),
            self.position[1] - (height*0.1),
            self.width * 1.2,
            self.height *1.2
        )

        self.rects = [self.normal_rect,
                      self.highlighted_rect]

    
    def update(self, mouse_pos, mouse_clicked):
        if self.normal_rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_clicked:
                return self.action
        else:
            self.mouse_over = False


    def draw(self, screen):
        if(self.mouse_over):
            pg.draw.rect(screen, self.color, self.rects[1],0, 25)
        else:
            pg.draw.rect(screen, self.color, self.rects[0],0, 25)
            