import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 100
BOARD_SIZE = 4

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define buttons
button_font = pygame.font.Font(None, 36)
player1_button = pygame.Rect(50, 500, 200, 50)
player2_button = pygame.Rect(300, 500, 200, 50)

current_player = None
player_selected = False
move_count = 0
red_count = 15
blue_count = 15

def draw_grid():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if board[row][col] is not None:
                color = RED if board[row][col] == 'Player 1' else BLUE
                tile_rect = pygame.Rect(rect.x, rect.y + CELL_SIZE - 20, CELL_SIZE, 20)
                pygame.draw.rect(screen, color, tile_rect)

def draw_buttons():
    pygame.draw.rect(screen, RED, player1_button)
    pygame.draw.rect(screen, BLUE, player2_button)
    player1_text = button_font.render('Player 1', True, WHITE)
    player2_text = button_font.render('Player 2', True, WHITE)
    screen.blit(player1_text, (player1_button.x + 50, player1_button.y + 10))
    screen.blit(player2_text, (player2_button.x + 50, player2_button.y + 10))

def draw_counts():
    count_font = pygame.font.Font(None, 36)
    red_count_text = count_font.render(f'Red Count: {red_count}', True, RED)
    blue_count_text = count_font.render(f'Blue Count: {blue_count}', True, BLUE)
    screen.blit(red_count_text, (600, 100))
    screen.blit(blue_count_text, (600, 150))

def check_winner():
    for row in range(BOARD_SIZE):
        if board[row][0] is not None and all(board[row][col] == board[row][0] for col in range(BOARD_SIZE)):
            return True
    return False

run = True
while run:
    screen.fill(WHITE)
    draw_grid()
    draw_counts()
    if not player_selected:
        draw_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if not player_selected:
                if player1_button.collidepoint(mouse_x, mouse_y):
                    current_player = 'Player 1'
                    player_selected = True
                elif player2_button.collidepoint(mouse_x, mouse_y):
                    current_player = 'Player 2'
                    player_selected = True
            elif current_player is not None:
                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE
                if row < BOARD_SIZE and col < BOARD_SIZE and board[row][col] is None:
                    if move_count < 2:
                        # First two moves: place the other player's color
                        board[row][col] = 'Player 2' if current_player == 'Player 1' else 'Player 1'
                        if current_player == 'Player 1':
                            blue_count -= 1
                        else:
                            red_count -= 1
                    else:
                        # Subsequent moves: place the current player's color
                        board[row][col] = current_player
                        if current_player == 'Player 1':
                            red_count -= 1
                        else:    
                            blue_count -= 1
                    move_count += 1
                    if check_winner():
                        print(f'{current_player} wins!')
                    else:
                    # Switch turns
                        current_player = 'Player 2' if current_player == 'Player 1' else 'Player 1'

    pygame.display.update()
pygame.quit()