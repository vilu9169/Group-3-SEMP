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
WHITE = (255, 255, 255)

class GameState(Enum):
    RED = -1
    TITLE = 0
    BLUE = 1
    
    PLACE = 2
    MOVE = 3

    INFO = 4

# Helper function that writes a text on a certain position in the game.
def text_creator(text, fontsize, color, pos, screen):
    font = pg.freetype.SysFont("Inter", fontsize, bold =False)
    rendered_text, _ = font.render(text, color)
    pg.draw.rect(screen,TURQUISE,rendered_text.get_rect(center=pos))
    textRect = rendered_text.get_rect(center = pos)
    screen.blit(rendered_text, textRect)

# Adds a text which tells whose turn it is
def whose_turn(screen, board):
    turn = board.whose_turn()
    text_creator(turn, 32, BLACK, (WINDOW_SIZE[0] // 2, 50), screen)

def pieces_left(screen, board, color):
    p1_left = str(board.piecesleft_blue)
    p2_left = str(board.piecesleft_red)
    color = RED if color == "red" else BLUE
    
    text_creator("Pieces left", 14, BLACK, (80, 500), screen)

    if (board.turn == "player1"):
        text_creator("Player 1:" + p1_left, 14, color, (80, 520), screen)
        text_creator("Player 2:" + p2_left, 14, BLACK, (80, 540), screen)
    else:
        text_creator("Player 1:" + p1_left, 14, BLACK, (80, 520), screen)
        text_creator("Player 2:" + p2_left, 14, color, (80, 540), screen)


# Generates the board and will control the game    
def generate_board(screen, board, color, round):
    if round == 0:
        board.color = color
    
    move_button =  ActionButton((225,550), 125, 75, WHITE, "Move", GameState.MOVE)
    place_button = ActionButton((425,550), 125, 75, WHITE, "Place", GameState.PLACE)
    info_button = ActionButton((625,250), 125, 75, WHITE, "Info", GameState.INFO)
    
    moves_buttons = [move_button, place_button, info_button]
    
    class Action(Enum):
        MOVE = 0
        PLACE = 1

    action = Action.MOVE
    screen.fill(TURQUISE)
    while True:
        
        # can be function? Same as in Title screen
        # this might not work for AI. Might use keyboard inputs instead of mouseclick!
        mouse_clicked = False
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_clicked = True
                board.handle_click(event, action)
                action = Action.MOVE
            if event.type == pg.QUIT:
                return False
    
            
        whose_turn(screen, board)
        pieces_left(screen, board, board.color)
                
        # can be a function? Same as in title screen

        for button in moves_buttons:
            ui_action = button.update(pg.mouse.get_pos(), mouse_clicked)
            if ui_action is not None:
                if ui_action == GameState.MOVE:
                    #...Call function in board...
                    print("TODO: Create MOVE function in board")
                    action = Action.MOVE
                elif ui_action == GameState.PLACE:
                    #...Call function in board...
                    action = Action.PLACE
                    print("TODO: Call PLACE function in board")
                elif ui_action == GameState.INFO:
                    #...Call function in board...
                    print("TODO: Call INFO function in board")
                    board.pop_up_rules(screen)
                else:
                    print("unnkown gamestate")
            button.draw(screen)
            
        #text_creator("Move", 25, BLACK, (285, 585), screen)
        #text_creator("Place", 25, BLACK, (485, 585), screen)
            
        board.draw_board(screen)
        pg.display.flip()
        

# Generates a titlescreen with two buttons for choosing color
def title_screen(screen):
    screen.fill(TURQUISE) 
    red_button = ActionButton((150,400), 150, 100, RED, "", GameState.RED)
    blue_button = ActionButton((500,400), 150, 100, BLUE, "", GameState.BLUE)

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
    i= 0
    while run:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)
            if not game_state:
                run = False
        if game_state == GameState.BLUE:
            run = generate_board(screen, board, "blue",i)
            game_state = GameState.BLUE
            

        if game_state == GameState.RED:
            run = generate_board(screen, board, "red",i)
            game_state = GameState.RED

        i+=1
            
                
if __name__ == "__main__":
    main()
