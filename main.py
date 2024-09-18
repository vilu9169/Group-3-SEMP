import pygame as pg
from data.classes.menu import Butt
from data.classes.menu import GameState
from data.classes.board import Board


WINDOW_SIZE = (800, 700)
BOARD_SIZE = (400, 400)

BLACK =(0,0,0)
RED = (228, 112, 112)
BLUE = (123, 111, 255)

#Adds a text which tells whose turn it is
def whose_turn(screen, board):
    font = pg.freetype.SysFont("Courier", 32, bold=True)
    turn = board.whose_turn()
    text, _ = font.render(turn, BLACK)
    textRect = text.get_rect(center = (WINDOW_SIZE[0] // 2, 50))
    screen.blit(text, textRect)


    
def generate_board(screen, board, color):
    board.color = color
    while(True):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
        screen.fill((181,225, 252))
        board.draw_board(screen)
        whose_turn(screen,board)
        pg.display.flip()
        


def title_screen(screen):
    screen.fill((181,225, 252)) 
    Button1 = Butt((150,400), 150, 100, RED, GameState.RED)
    Button2 = Butt((500,400), 150, 100, BLUE, GameState.BLUE)
    # action1 = Button1.update(pg.mouse.get_pos(), mouse_clicked)
    # action2 = Button2.update(pg.mouse.get_pos(), mouse_clicked)
    # Button1.draw(screen)
    # Button2.draw(screen)

    buttons = [Button1, Button2]
    while True:
        mouse_clicked = False
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_clicked = True
            if event.type == pg.QUIT:
                return False
        screen.fill((181,225, 252))

        font = pg.freetype.SysFont("Inter", 55, bold =False)
        text, _ = font.render("UU game", BLACK)
        textRect = text.get_rect(center = (WINDOW_SIZE[0] // 2, 100))
        screen.blit(text, textRect)

        font = pg.freetype.SysFont("Inter", 30, bold =False)
        text, _ = font.render("Player 1, pick a color to start!!!", BLACK)
        textRect = text.get_rect(center = (WINDOW_SIZE[0] // 2, 180))
        screen.blit(text, textRect)


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


    run = True
    game_state  = GameState.TITLE

    while(run):
        if game_state == GameState.TITLE:
            
            game_state = title_screen(screen)
            if(not game_state):
                run = False
            
        if game_state == GameState.BLUE:
            run = generate_board(screen, board, "blue")
            game_state = GameState.BLUE

        if game_state == GameState.RED:
            run = generate_board(screen, board, "red")
            game_state = GameState.RED
                
if __name__ == "__main__":
    main()
