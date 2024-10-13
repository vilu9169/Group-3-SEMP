import pygame as pg
from data.classes.gamestate import GameState
# from main import text_creator
BLACK = (0,0,0)
INACTIVE_COLOR = (128,128,128)
ACTIVE_COLOR = (255, 255, 255)

class Input:
    def __init__(self, x,y, width, height, number=""):
        self.input_box = pg.Rect(x, y, width, height)
        self.active =  False
        self.number = number
        self.pos = (x,y)
        self.color = INACTIVE_COLOR
        self.done = False



    
    def handle_event(self, event, stack_size):
        if event.type == pg.KEYDOWN:
            number = event.unicode
            if number.isnumeric(): 
                if(1 < int(number) < stack_size +1):
                    self.number += event.unicode
                    return int(number)
        print("Wrong move")
        return None
                # Re-render the text.



        