import pygame as pg
import time
from enum import Enum
from data.classes.gamestate import GameState
from data.classes.gamestate import GameInit
from data.classes.button import ActionButton
from data.classes.board import Board
from data.classes.input import Input
from AI.GameAI import AI_first_move, iterative_deepening
from data.classes.AI_translations import board_translation, inverse_board_translation
from AI.board import load_transposition_table

TRANSPOSITION_TABLE = load_transposition_table()

DIRECTION_MAP = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0)
}

WINDOW_SIZE = (800, 700)
BOARD_SIZE = (400, 400)

BLACK =(0,0,0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TURQUISE = (181,225, 252)
WHITE = (255, 255, 255)
GREY = (128,128,128)
GREEN = (31, 194, 50)


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
    board.check_win()
    if round == 0:
        board.p1_color = color
        board.color = color

    # if AI och palyer 2
    if (board.AIopponent and board.turn == "player2"):
        reset_rect = pg.Rect(0, 65, WINDOW_SIZE[0], 30)
        text_creator("AI is cooking... (let him cook)", 14, BLACK, (WINDOW_SIZE[0] // 2, 80), screen, reset_rect)
        ai_board = board_translation(board)
        pg.display.update(reset_rect)  # we generate text, we dont have to worry about removing it since the main system prompts will overrite

        # if första runda:
        if (board.piecesleft_blue == 15 or board.piecesleft_red == 15):
            print("AI is thinking")
            time.sleep(2)
            action = AI_first_move(ai_board, 2, 2, board.piecesleft_blue, board.piecesleft_red)
            print("AI first move")
        else:

            action = iterative_deepening(ai_board, 2, 2, board.piecesleft_red, board.piecesleft_blue, 4, True, TRANSPOSITION_TABLE, time_limit= board.difficulty)

            print("iterative_deepening")
        
        # om det är en move
        if len(action) == 7:
            print("move")
            current_pos = (action[2],action[1])

            direction_tuple = DIRECTION_MAP[action[4]]
            direction_tuple = tuple(i * len(action[5]) for i in direction_tuple)
            new_pos = (current_pos[0] + direction_tuple[0], current_pos[1] + direction_tuple[1])
            piece = board.get_piece_from_pos(current_pos)
            current_square = board.get_square_from_coord(current_pos)
            if len(current_square.pieces) > 1:
                # piece = current_square.pieces[action[3]]
                piece.stack_piece_index =  action[3] -1
            new_square = board.get_square_from_coord(new_pos)
            piece.valid.append(new_square)
            piece.move(new_square, board)
            
        # om det är en place
        elif len(action) == 3:
            print("place")
            does_stand = False if action[0] == "lay" else True
            board.populate((action[2],action[1]), does_stand)
            
        # new_turn
        board.new_turn()
        return True
    
    move_button =  ActionButton((225,550), 125, 75, WHITE, "Move", GameState.MOVE) if board.piecesleft_blue < 15 and board.piecesleft_red < 15 else ActionButton((225,550), 125, 75, GREY, "Move", None)
    place_button = ActionButton((425,550), 125, 75, WHITE, "Place", GameState.PLACE)
    info_button = ActionButton((625,250), 125, 75, WHITE, "Info", GameState.INFO)
    input_bar = Input(WINDOW_SIZE[0]//2 - 50 ,650, 100, 25)
    board.input = input_bar

    
    moves_buttons = [move_button, place_button, info_button]

    screen.fill(TURQUISE)

    
    # can be function? Same as in Title screen
    # this might not work for AI. Might use keyboard inputs instead of mouseclick!
    mouse_clicked = False
    
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONUP:
            mouse_clicked = True
            board.handle_click(event,screen)
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
                board.pop_up_rules(screen)

            else:
                print("unknown gamestate")
        button.draw(screen)
    
    board.draw_board(screen) 

    if (board.win is not None):
        board.action = GameInit.FINISHED
        return True
        


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

def difficulty_screen(screen):
    screen.fill(TURQUISE) 
    easy_button = ActionButton((150,400), 150, 100, GREEN, "easy", GameInit.EASY) #gameinit.easy
    medium_button = ActionButton((500,400), 150, 100, GREY, "medium", GameInit.MEDIUM) #gameinit.medium
    hard_button = ActionButton((150,550), 150, 100, RED, "hard", GameInit.HARD) #gameinit.hard
    buttons = [easy_button, medium_button, hard_button]
    while True:
        mouse_clicked = False
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_clicked = True
            if event.type == pg.QUIT:
                return GameInit.EXIT
        screen.fill(TURQUISE)

        text_creator("Choose the difficulty level", 30, BLACK, (WINDOW_SIZE[0] // 2, 200), screen)
        
        for button in buttons:
            ui_action = button.update(pg.mouse.get_pos(), mouse_clicked)
            if ui_action is not None:
                return ui_action
            button.draw(screen)
        pg.display.flip()




def restart_screen(screen, board):
    screen.fill(TURQUISE) 
    play_again_button = ActionButton((150,400), 150, 100, GREEN, "Play again", GameInit.CHOOSEOPPONENT)
    exit_button = ActionButton((500,400), 150, 100, GREY, "Exit", GameInit.EXIT)

    buttons = [play_again_button, exit_button]
    while True:
        mouse_clicked = False
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_clicked = True
            if event.type == pg.QUIT:
                return GameInit.EXIT
        screen.fill(TURQUISE)

        text_creator(board.win + " won!", 50, BLACK, (WINDOW_SIZE[0] // 2, 140), screen)
        text_creator("Choose whether to play again or exit the game", 30, BLACK, (WINDOW_SIZE[0] // 2, 200), screen)
        
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

def chooseOpponent(screen, board):
    print("Vi kommer hit")
    screen.fill(TURQUISE)
    print("vi kommer hit också")
    human_button = ActionButton((150,400), 150, 100, WHITE, "Human", GameInit.HUMAN)
    ai_button = ActionButton((500,400), 150, 100, WHITE, "AI", GameInit.AI)

    buttons = [human_button, ai_button]
    while True:
        mouse_clicked = False
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_clicked = True
            if event.type == pg.QUIT:
                return GameInit.EXIT
        screen.fill(TURQUISE)
        
        text_creator("Choose whether to play against an AI or a human", 30, BLACK, (WINDOW_SIZE[0] // 2, 200), screen)
        
        for button in buttons:
            ui_action = button.update(pg.mouse.get_pos(), mouse_clicked)
            if ui_action is not None:
                print(ui_action)
                return ui_action
            button.draw(screen)
        
        pg.display.flip()
        

def main():
    pg.init()
    screen = pg.display.set_mode(WINDOW_SIZE)
    board = None
    game_state  = GameInit.CHOOSEOPPONENT

    run = True
    i= 0
    while run:
        if game_state == GameInit.CHOOSEOPPONENT:
            board = Board(BOARD_SIZE[0], BOARD_SIZE[1])
            game_state = chooseOpponent(screen, board)
        
        if game_state == GameInit.AI:
            board.AIopponent = True
            game_state = GameInit.DIFFICULTY

        elif game_state == GameInit.HUMAN:
            board.AIopponent = False
            game_state = GameInit.TITLE

        if game_state == GameInit.DIFFICULTY:
            game_state = difficulty_screen(screen)

        if game_state == GameInit.EASY:
            board.difficulty = 5
            game_state = GameInit.TITLE
        elif game_state == GameInit.MEDIUM:
            board.difficulty = 10
            game_state = GameInit.TITLE
        elif game_state == GameInit.HARD:
            board.difficulty = 20
            game_state = GameInit.TITLE
        
        if game_state == GameInit.TITLE:
            i = 0
            game_state = title_screen(screen)
            if not game_state:
                run = False

        

        if game_state == GameInit.BLUE:
            run = generate_board(screen, board, "blue",i)
            game_state = GameInit.BLUE
            if board.action == GameInit.FINISHED:
                game_state = board.action
            
        if game_state == GameInit.RED:
            run = generate_board(screen, board, "red",i) 
            game_state = GameInit.RED
            if board.action == GameInit.FINISHED:
                game_state = board.action

        if game_state == GameInit.FINISHED:
            game_state = restart_screen(screen, board)

        if game_state == GameInit.EXIT:
            run = False

        i+=1
                
if __name__ == "__main__":
    main()