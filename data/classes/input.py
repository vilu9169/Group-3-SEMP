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



    
    def handle_event(self, event, stack, board):
        """
        Recieves move stack index from user and returns it if it is a valid move stack number
        """
        stack_size = len(stack)
        if event.type == pg.KEYDOWN:
            number = event.unicode
            if number.isnumeric(): 
                if(0 < int(number) < stack_size+1):
                    if(stack[int(number) - 1].color == board.color ):
                        #player is trying to move a piece within a stack and with the same color as player
                        self.number += event.unicode
                        return int(number) -1
        return None



        