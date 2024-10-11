import pygame as pg
from enum import Enum
from data.classes.gamestate import GameState
from data.classes.gamestate import GameInit
from data.classes.button import ActionButton
from data.classes.board import Board


WINDOW_SIZE = (800, 700)
BOARD_SIZE = (400, 400)

BLACK =(0,0,0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TURQUISE = (181,225, 252)
WHITE = (255, 255, 255)
GREY = (128,128,128)


# Helper function that writes a text on a certain position in the game.
def text_creator(text, fontsize, color, pos, screen, rect = None):
    font = pg.freetype.SysFont("Inter", fontsize, bold =False)
    rendered_text, _ = font.render(text, color)
    textRect = rendered_text.get_rect(center = pos)
    if rect is not None:
        pg.draw.rect(screen,TURQUISE,rect)
    else:
        pg.draw.rect(screen,TURQUISE,textRect)
    screen.blit(rendered_text, textRect)

# Adds a text which tells whose turn it is
def whose_turn(screen, board):
    turn = board.whose_turn()
    description = "Please choose what to do"
    text = ""
    move_description = "Please select a piece to move"
    place_description = "Choose where you want to place your piece"
    first_place_description = "Place opponents piece"
    player1_win ="Player 1 wins"
    player2_win = "Player 2 wins"
    reset_rect = pg.Rect(0, 65, WINDOW_SIZE[0], 30)

    text_creator(turn, 32, board.color, (WINDOW_SIZE[0] // 2, 50), screen)
    
    if board.action is None:
        text = description
    elif board.action == GameState.MOVE:
        text = move_description
    elif board.action == GameState.PLACE and (board.piecesleft_blue == 15 or board.piecesleft_red == 15):
        text = first_place_description
    elif board.action == GameState.PLACE:
        text = place_description
    if board.win is not None:
        if board.win == "player1":
            text = player1_win
        if board.win == "player2":
            text = player2_win
    
    text_creator(text, 14, BLACK, (WINDOW_SIZE[0] // 2, 80), screen, reset_rect)
    


def pieces_left(screen, board, color):
    p1_left = str(board.piecesleft_blue)
    p2_left = str(board.piecesleft_red)
    color = RED if color == "red" else BLUE
    
    text_creator("Pieces left:", 14, BLACK, (80, 500), screen)

    reset_rect = pg.Rect(30, 510, 100, 90)
    if (board.turn == "player1"):
        text_creator("Player 1:" + p1_left, 14, color, (80, 520), screen, reset_rect)
        text_creator("Player 2:" + p2_left, 14, BLACK, (80, 540), screen)
    else:
        text_creator("Player 1:" + p1_left, 14, BLACK, (80, 520), screen,reset_rect)
        text_creator("Player 2:" + p2_left, 14, color, (80, 540), screen)


# Generates the board and will control the game    
def generate_board(screen, board, color, round):
    if round == 0:
        board.color = color
    
    move_button =  ActionButton((225,550), 125, 75, WHITE, "Move", GameState.MOVE) if board.piecesleft_blue < 15 and board.piecesleft_red < 15 else ActionButton((225,550), 125, 75, GREY, "Move", None)
    place_button = ActionButton((425,550), 125, 75, WHITE, "Place", GameState.PLACE)
    info_button = ActionButton((625,250), 125, 75, WHITE, "Info", GameState.INFO)
    
    moves_buttons = [move_button, place_button, info_button]

    screen.fill(TURQUISE)

    
    # can be function? Same as in Title screen
    # this might not work for AI. Might use keyboard inputs instead of mouseclick!
    mouse_clicked = False
    
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONUP:
            mouse_clicked = True
            board.handle_click(event, screen)
        if event.type == pg.QUIT:
            return False

      
    whose_turn(screen, board)
    pieces_left(screen, board, board.color)
            
    # can be a function? Same as in title screen

    for button in moves_buttons:
        ui_action = button.update(pg.mouse.get_pos(), mouse_clicked)
        if ui_action is not None:
            if ui_action == GameState.MOVE:
                board.action = GameState.MOVE
            elif ui_action == GameState.PLACE:
                board.action = GameState.PLACE
            elif ui_action == GameState.INFO:
                board.action = GameState.INFO
                board.pop_up_rules(screen)
            else:
                print("unknown gamestate")
        button.draw(screen)
    
    board.draw_board(screen) 

    if (board.win is not None):
        return False
        


    pg.display.update()
    return True
    

# Generates a titlescreen with two buttons for choosing color
def title_screen(screen):
    screen.fill(TURQUISE) 
    red_button = ActionButton((150,400), 150, 100, RED, "", GameInit.RED)
    blue_button = ActionButton((500,400), 150, 100, BLUE, "", GameInit.BLUE)

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
        
def restart_screen(screen):
    screen.fill(TURQUISE) 
    play_again_button = ActionButton((150,400), 150, 100, RED, "", GameInit.TITLE)
    exit_button = ActionButton((500,400), 150, 100, GREY, "", None)

    buttons = [play_again_button, exit_button]
    while True:
        mouse_clicked = False
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_clicked = True
            if event.type == pg.QUIT:
                return False
        screen.fill(TURQUISE)

        text_creator("Choose whether to play again or exit the game", 30, BLACK, (WINDOW_SIZE[0] // 2, 100), screen)

        for button in buttons:
            ui_action = button.update(pg.mouse.get_pos(), mouse_clicked)
            if ui_action is GameInit.TITLE:
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
    game_state  = GameInit.TITLE

    run = True
    i= 0
    while run:
        if game_state == GameInit.TITLE:
            game_state = title_screen(screen)
            if not game_state:
                run = False
        if game_state == GameInit.BLUE:
            run = generate_board(screen, board, "blue",i)
            game_state = GameInit.BLUE
            

        if game_state == GameInit.RED:
            run = generate_board(screen, board, "red",i) 
            game_state = GameInit.RED
        i+=1

        if run == False:
            print("vi kommer hit!")
            game_state = restart_screen(screen)
            print(game_state)
            if game_state == GameInit.TITLE:
                run = True
                continue

                
if __name__ == "__main__":
    main()
