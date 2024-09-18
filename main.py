import pygame as pg

from data.classes.board import Board

WINDOW_SIZE = (500, 500)

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])
screen = pg.display.set_mode(WINDOW_SIZE)


#def generate_board
def generate_board(screen):
    screen.fill((181,225, 252))
    board.draw_board(screen)
    pg.display.update()


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

