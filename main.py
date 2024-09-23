import pygame as pg
from enum import Enum

from data.classes.button import ActionButton
from data.classes.board import Board


WINDOW_SIZE = (800, 700)
BOARD_SIZE = (400, 400)

BLACK =(0,0,0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TURQUISE = (181,225, 252)

class GameState(Enum):
    RED = -1
    TITLE = 0
    BLUE = 1


#Helper function that writes a text on a certain position in the game.
def text_creator(text, fontsize, color, pos, screen):
    font = pg.freetype.SysFont("Inter", fontsize, bold =False)
    rendered_text, _ = font.render(text, color)
    textRect = rendered_text.get_rect(center = pos)
    screen.blit(rendered_text, textRect)

#Adds a text which tells whose turn it is
def whose_turn(screen, board):
    turn = board.whose_turn()
    text_creator(turn, 32, BLACK, (WINDOW_SIZE[0] // 2, 50), screen)

#Generates the board and will control the game    
def generate_board(screen, board, color):
    board.color = color
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
        screen.fill(TURQUISE)
        board.draw_board(screen)
        whose_turn(screen,board)
        pg.display.flip()
        

#Generates a titlescreen with two buttons for choosing color
def title_screen(screen):
    screen.fill(TURQUISE) 
    red_button = ActionButton((150,400), 150, 100, RED, GameState.RED)
    blue_button = ActionButton((500,400), 150, 100, BLUE, GameState.BLUE)

    buttons = [red_button, blue_button]
    while True:
        mouse_clicked = False
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_clicked = True
            if event.type == pg.QUIT:
                return False
        screen.fill(TURQUISE)

        text_creator("UU game", 55, BLACK, (WINDOW_SIZE[0] // 2, 100), screen)
        text_creator("Player 1, pick a color to start!!!", 30, BLACK, (WINDOW_SIZE[0] // 2, 180), screen)

        for button in buttons:
            ui_action = button.update(pg.mouse.get_pos(), mouse_clicked)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pg.display.flip()
        

 
# set the center of the rectangular object.
#def choose_player
#def start_game
#def gameover_page

def main():
    pg.init()
    screen = pg.display.set_mode(WINDOW_SIZE)
    board = Board(BOARD_SIZE[0], BOARD_SIZE[1])
    game_state  = GameState.TITLE

    run = True
    while run:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)
            if not game_state:
                run = False
            
        if game_state == GameState.BLUE:
            run = generate_board(screen, board, "blue")
            game_state = GameState.BLUE

        if game_state == GameState.RED:
            run = generate_board(screen, board, "red")
            game_state = GameState.RED
                
if __name__ == "__main__":
    main()
