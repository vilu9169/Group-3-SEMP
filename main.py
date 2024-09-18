import pygame as pg
from data.classes.board import Board


WINDOW_SIZE = (800, 700)
BOARD_SIZE = (400, 400)
board = Board(BOARD_SIZE[0], BOARD_SIZE[1])
screen = pg.display.set_mode(WINDOW_SIZE)

black =(0,0,0)

#Adds a text which tells whose turn it is
def whose_turn(screen):
    pg.font.init()
    font = pg.font.Font('freesansbold.ttf', 32)
    turn = board.whose_turn()

    text = font.render(turn, True, black)
    textRect = text.get_rect()
    textRect.center = (WINDOW_SIZE[0] // 2, 50)
    screen.blit(text, textRect)



#def generate_board
def generate_board(screen):
    screen.fill((181,225, 252))
    board.draw_board(screen)
    whose_turn(screen)
    pg.display.update()


 
# set the center of the rectangular object.
#def choose_player
#def start_game
#def gameover_page
if __name__ == "__main__":
    run = True
    while(run):
        pg.init()
        generate_board(screen)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
