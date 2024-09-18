import pygame as pg
from data.classes.menu import Butt
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


    
def generate_board(screen, board):
    screen.fill((181,225, 252))
    board.draw_board(screen)
    whose_turn(screen,board)
    pg.display.update()

def title_screen(screen, mouse_clicked):
    screen.fill((181,225, 252)) 
    Button1 = Butt((150,400), 150, 100, RED)
    Button2 = Butt((500,400), 150, 100, BLUE)
    Button1.update(pg.mouse.get_pos(), mouse_clicked)
    Button1.draw(screen)
    Button2.update(pg.mouse.get_pos(), mouse_clicked)
    Button2.draw(screen)



 
# set the center of the rectangular object.
#def choose_player
#def start_game
#def gameover_page

def main():


    screen = pg.display.set_mode(WINDOW_SIZE)
    board = Board(BOARD_SIZE[0], BOARD_SIZE[1])
    pg.init()
    run = True

    while(run):
        mouse_clicked = False
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_clicked = True
            if event.type == pg.QUIT:
                run = False
        # generate_board(screen, board)
        title_screen(screen, mouse_clicked)
        pg.display.update()
                
if __name__ == "__main__":
    main()
