import ast
import sys
import copy
import pickle
import os
import re
import AI.GameAI as GameAI
import AI.MoveGenerator as MoveGenerator
from collections import deque
from AI.threat_assessment_2p import get_valid_edge_pieces, define_finish_edges
from AI.evaluation import pieces_left
import AI.evaluation as evaluation

## Current problems:
# Sometimes, player 1 and human is used interchangably, same goes for player 2 
# and AI This will make it messy to implement having the AI go as first player 
# in the current state of the code.

# EXAMPLE FOR THE BOARD ABSTRACTION:
# First element of the list is an indicator, which tells the status of the
# top stone:
# 0 = lying stone (which also means we can play any stone in this spot)
# 1 = standing stone (which also means we can NOT play any stone in this spot)
# Subsequent elements are stones:
# 2 = red stones (Player 1)
# 3 = blue stones (Player 2)

# [1, 2,2,2,3 ] example of a single square containing 3 lying red stones, and
# 1 standing blue stone on top

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# Directions mapping
direction_map = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}

# Tuple to keep track of the first moves of the players, first one is for player 1, second one is for AI
first_moves = (True, True)

current_player = 1
opponentAI = 2

playing_against_AI = False

player1_stone_reserves = 15
player2_stone_reserves = 15

def print_usage(program):
    """ Prints information on how to run the program. """
    print(f"Usage: {program} [BOARD_FILE]")

def has_txt_format(filename):
    """Checks if a filename ends with .txt"""
    return filename.endswith(".txt")

# Path to save the transposition table
TRANS_TABLE_PATH = "transposition_table.pkl"

def save_transposition_table(table):
    with open(TRANS_TABLE_PATH, 'wb') as f:
        pickle.dump(table, f)

def load_transposition_table():
    if os.path.exists(TRANS_TABLE_PATH):
        with open(TRANS_TABLE_PATH, 'rb') as f:
            return pickle.load(f)
    return {}

transposition_table = load_transposition_table()

# Function to read board from a text file
def read_board(filename):
    """ Read board given by filename."""
    board = []
    with open(filename, 'r') as file:
        for line in file:
            # Parse the line into a list (from string to Python object)
            board.append(ast.literal_eval(line.strip()))
    # Check if the board is a square board
    if not is_square_board(board):
        raise ValueError("The board is not a square (n x n) board.")

    return board

def is_square_board(board):
    """Check if the board is a square board."""
    n = len(board)
    return all(len(row) == n for row in board)

def sanitize_filename(filename):
    """Replaces restricted characters with underscores"""
    return re.sub(r'[\\/:*?"<>|]', '_', filename)

def write_board(filename, board):
    """ Write the board to a file with given filename. """

    filename = sanitize_filename(filename)

    with open(filename, 'w') as file:
        for row in board:
            file.write(str(row) + '\n')

def dynamic_padding(board):
    """ Creates dynamic padding between the letters of the board columns.
        This is purely cosmetic so that the board prints nicer."""
    max_length = 0

    for row in board:
        for col in row:
            max_length = max(max_length, len(col))

    padding = "   " + " " * max_length
    return padding

def print_board(board):
    """ Prints the board. """
    cols = len(board[0])
    board_head = ""

    padding = dynamic_padding(board)

    for col in range(cols):
        board_head += padding
        board_head += alpha[col]
    print(board_head)

    init_num = 1
    for row in board:
        print(f'{init_num} {row}')
        init_num += 1


def print_help_info():
    """ Prints the available actions. """
    print("Available actions:")
    print("lay - place a lying stone on the board")
    print("stand - place a standing stone on the board")
    print("move - move a stack of stones on the board")
    print("help - show this help message")
    print("exit - quit the game")
    print("Or you can also type the first letter of any action above")


def select_square(board):
    """ Lets the user select a valid square within the board via input. """
    InvalidInput = True
    while InvalidInput:
        try:
            row = int(input('Row: ').strip()) - 1
            col = input('Column: ').strip().upper()
            if col in alpha:
                col = alpha.index(col)
                if is_out_of_bounds(board, row, col):
                    print(f'Invalid input. Please enter a valid row (1-{len(board)}) and column (A-{alpha[len(board)-1]}).')
                else:
                    InvalidInput = False
            else:
                print(f'Invalid input. Please enter a valid row (1-{len(board)}) and column (A-{alpha[len(board)-1]}).')
        except ValueError or TypeError:
            print(f'Invalid input. Please enter a valid row (1-{len(board)}) and column (A-{alpha[len(board)-1]}).')
    return row, col

def stone_is_placeable(board):
    """ Returns true if there is any spot on the board where a stone can be placed. """
    stone_is_placeable = False
    for row in board:
        for col in row:
            if col[0] == 0:
                stone_is_placeable = True
    return stone_is_placeable

def player_has_movable_stack(board, current_player):
    """ Returns true if there is any spot on the board where a player has
        a moveable stack. """
    global direction_map, alpha
    player_has_movable_stack = False
    for row_index, row in enumerate(board):
        for col_index, square in enumerate(row):
            if (current_player + 1) in square:
                for (move_row, move_col) in direction_map.values():
                    new_row = row_index + move_row
                    new_col = col_index + move_col
                    if is_out_of_bounds(board,new_row,new_col):
                        continue
                    if board[new_row][new_col][0] == 0:
                        player_has_movable_stack = True

    return player_has_movable_stack

def place_stone(board, current_player, standing=False):
    """ Function which asks the user for a location in which to place a stone,
        before this, it must be decided if the stone will be lying or standing. """
    global alpha, first_moves, player1_stone_reserves, player2_stone_reserves
    print_board(board)

    current_stack = [1]
    while current_stack[0] != 0:
        print(f"Where do you want to place the stone?")
        row, col = select_square(board)
        current_stack = board[row][col]
        if current_stack[0] != 0:
            print(f"Error: There is a standing stone at row {row+1}, column {alpha[col]}. Please select another position.")
    # Place the player's stone on top of the stack
    if first_moves[0]:
        # handle placing opponents stone on 2 first placements
        current_stack.append(current_player + 2)
        player2_stone_reserves -= 1
    else:
        # handle placing opponents stone on 2 first placements
        if first_moves[1] and not playing_against_AI:
            first_moves = (first_moves[0], False)
            current_stack.append(current_player)
            player1_stone_reserves -= 1
        
        else: # else it's just a regular placement
            current_stack.append(current_player + 1)
            if current_player == 1:
                player1_stone_reserves -= 1 
            else: 
                player2_stone_reserves -= 1
    if standing:
        current_stack[0] = 1
        print(f"Player {current_player} placed a standing stone at row {row+1}, column {alpha[col]}.")
    else:
        print(f"Player {current_player} placed a lying stone at row {row+1}, column {alpha[col]}.")

def place_stoneAI(board, row, col, current_player, standing=False):
    global alpha, first_moves, player2_stone_reserves, player1_stone_reserves
    
    current_stack = board[row][col]
    if current_player == 2:
        player2_stone_reserves -= 1
    else:
        player1_stone_reserves -= 1
        
    if current_stack[0] == 0:
        # Place the player's stone on top of the stack
        
        current_stack.append(current_player + 1)
        if standing:
            current_stack[0] = 1

def get_allowed_stack_sizes(current_stack, current_player, last_stack_size=None):
    """ Get the allowed movable substack sizes, filtering based on the last stack size if provided. """
    allowed_moving_stack_indexes = []
    
    for i in range(len(current_stack)):
        if current_stack[i] == current_player + 1:
            allowed_moving_stack_indexes.append(i)
    
    allowed_sizes = [len(current_stack) - i for i in allowed_moving_stack_indexes]
    
    # Filter allowed sizes to be strictly less than last_stack_size if it exists
    if last_stack_size is not None:
        allowed_sizes = [size for size in allowed_sizes if size < last_stack_size]

    return allowed_sizes

def is_out_of_bounds(board, row, col):
    """Check if a position is out of the board bounds."""
    return row < 0 or row >= len(board) or col < 0 or col >= len(board[0])

def move_stack(board, current_player, row, col):
    global alpha, direction_map

    def update_board_after_move(old_row, old_col, new_row, new_col, stack_size, indicator):
        """Update the board by moving a stack from old position to new position."""
        moving_stack = board[old_row][old_col][-stack_size:]
        board[old_row][old_col] = board[old_row][old_col][:-stack_size]
        board[new_row][new_col].extend(moving_stack)
        if indicator == 1:  # if stack we are moving has standing stone
            board[old_row][old_col][0] = 0  # old location loses standing stone on top
            board[new_row][new_col][0] = 1  # new location gains standing stone on top

    def get_next_position(row, col, direction):
        """Calculate the next position based on the direction."""
        move_row, move_col = direction_map[direction]
        return row + move_row, col + move_col

    def get_move_direction(row,col):
        """Get a valid move direction from the user."""
        while True:
            direction = input('Which direction do you want to move the stack? (up/down/left/right): ').strip().lower()
            if direction in direction_map:
                next_row, next_col = get_next_position(row,col,direction)
                if is_out_of_bounds(board, next_row, next_col) or board[next_row][next_col][0] == 1:
                    direction = None
                else:
                    return direction
            print("Error: Invalid direction. Please enter up, down, left, or right.")

    def get_stack_size(allowed_sizes):
        """Get a valid stack size from the user."""
        while True:
            print(f'You can move any of these amounts of stones: {allowed_sizes}')
            size = input('How many stones do you want to move?: ').strip()
            if size.isdigit() and int(size) in allowed_sizes:
                return int(size)
            print(f"Error: Invalid stack size. Please select a stack size from the allowed stack sizes: {allowed_sizes}.")

    print_board(board)

    # Main move logic
    current_stack = board[row][col][1:]  # Remove indicator temporarily
    indicator = board[row][col][0]
    last_stack_size = None
    direction = None

    while True:
        allowed_sizes = get_allowed_stack_sizes(current_stack, current_player, last_stack_size)

        stack_size = get_stack_size(allowed_sizes)

        if direction == None:
            direction = get_move_direction(row, col)

        next_row, next_col = get_next_position(row, col, direction)

        next_stack_size = len(board[next_row][next_col]) - 1

        update_board_after_move(row, col, next_row, next_col, stack_size, indicator)
        print(f"Moved stack to ({next_row+1}, {alpha[next_col]}).")
        print_board(board)

        row, col = get_next_position(row, col, direction)
        next_row, next_col = get_next_position(row, col, direction)

        if is_out_of_bounds(board, next_row, next_col):
            print("Next spot is out of bounds. Movement terminated.")
            break

        if board[next_row][next_col][0] == 1:
            print("Next spot has standing stone. Movement terminated.")
            break

        current_stack = board[row][col][next_stack_size:]
        allowed_sizes = get_allowed_stack_sizes(current_stack, current_player)

        last_stack_size = stack_size

        if (not allowed_sizes) or (len(allowed_sizes) == 1 and allowed_sizes == [last_stack_size]):
            print("No valid stack size left. Movement terminated.")
            break

        # Ask if user wants to continue moving
        move_again = None
        while move_again not in ['y', 'yes', 'n', 'no']:
            move_again = input('Do you want to move one more step? (y/yes/n/no): ').strip().lower()
            if move_again not in ['y', 'yes', 'n', 'no']:
                print('Invalid input. Try again.')
        if move_again in ['n','no']:
            break


    print("Stack movement completed.")

def move_stackAI(board, row, col, start, direction, sequence, standing):
    global direction_map
    # Get the stack the player should move
    stack_to_move = board[row][col][start:]
    # Go through drop sequence
    new_row = row
    new_col = col
    count = 0
    for drop in sequence:
        # Take one step
        new_row += direction_map[direction][0]
        new_col += direction_map[direction][1]
        # Drop the correct amount of pieces on that square
        board[new_row][new_col] += stack_to_move[:drop]
        count += drop
    board[row][col] = board[row][col][:start]
    board[new_row][new_col] += stack_to_move[count:]
    
    if standing:
        board[new_row][new_col][0] = 1
        board[row][col][0] = 0

def apply_action(board, action, player):
    # lay action = ['lay', row, col]
    if action[0] == 'lay':
        place_stoneAI(board, action[1], action[2], player)
    # Stand action = ['stand', row, col]
    elif action[0] == 'stand':
        place_stoneAI(board, action[1], action[2], player, standing=True)
    # Move action = ['move', row, col, start, direction, sequence, isStanding]
    elif action[0] == 'move':
        move_stackAI(board, action[1], action[2], action[3], action[4], action[5], action[6])
    return board
    
def check_win_conditions(board, player, player_reserves):
    """
    Function to check if a player has won the game by reaching the opposite side of the board
    * The function uses a breadth-first search to find all possible paths
    * Returns a triple: (win, player, path) where win is a boolean indicating if a player has won
    """
    moves = MoveGenerator.generate_moves(board, player, player_reserves)
    if len(moves) == 0:
        flats_diff = evaluation.flats_differential(board, player)
        if player == 2:
            winner = player+1 if flats_diff > 0 else player
        else:
            winner = player+1 if flats_diff > 0 else player+2
        return [True, winner, []]
    
    edge_pieces = get_valid_edge_pieces(board)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for piece in edge_pieces:
        start_row, start_col = piece[0], piece[1]

        # Check if the start position is valid (not empty)
        if len(board[start_row][start_col]) < 2:
            #print("No piece placed on start") # Commented out for now
            continue

        player = board[start_row][start_col][-1]

        queue = deque([(start_row, start_col, 0, [(start_row, start_col)])])
        visited = set([(start_row, start_col)])

        # Based on the start position, define the finish edges
        finish_edges = define_finish_edges(
            start_row, start_col, len(board), len(board[0]))

        # BFS search
        while queue:
            row, col, dist, path = queue.popleft()

            if (row, col) in finish_edges:
                return (True, player, path)

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc

                if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]) and (new_row, new_col) not in visited:
                    if board[new_row][new_col][0] == 1 or board[new_row][new_col][-1] != player:
                        continue

                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col, dist + 1,
                                 path + [(new_row, new_col)]))
    return (False, None, [])

def game_loop(board, current_player):
    """ Main game-loop where the game is played out until some condition
        triggers the end of the game, either by board getting won, or no more
        moves are able to be made (stalemate)."""
    global alpha, first_moves, player1_stone_reserves, player2_stone_reserves, playing_against_AI, transposition_table
    
    stones_left = player1_stone_reserves if current_player == 1 else player2_stone_reserves
    
    if playing_against_AI:
        opponent_stones_left = player2_stone_reserves
    else:
        opponent_stones_left = player2_stone_reserves if current_player == 1 else player1_stone_reserves

    print(f'It\'s your time to make a move, Player {current_player}.')
    print(f'You currently have {stones_left} unplaced stones left.')
    move = input('What move do you want to make?: ').strip().lower()

    if move ==   'h':
        move = 'help'
    elif move == 'e':
        move = 'exit'
    elif move == 'l':
        move = 'lay'
    elif move == 'm':
        move = 'move'
    elif move == 's':
        move = 'stand'
    else:
        None

    successful_move = True
    match move:
        case "help":
            print_help_info()
            successful_move = False
        case "lay":
            if not stone_is_placeable(board):
                print("Error: No spaces left on board to place a stone in.")
                successful_move = False
            if current_player == 1 and player1_stone_reserves == 0:
                print("Error: Player 1 has no stones left to place.")
                successful_move = False
            elif current_player == 2 and player2_stone_reserves == 0:
                print("Error: Player 2 has no stones left to place.")
                successful_move = False
            else:
                place_stone(board, current_player)

            if successful_move:
                if not playing_against_AI:
                    current_player = 2 if current_player == 1 else 1
                if first_moves[0]:
                    first_moves = (False, first_moves[1])

        case "stand":
            if not stone_is_placeable(board):
                print("Error: No spaces left on board to place a stone in.")
                successful_move = False
            if current_player == 1 and player1_stone_reserves == 0:
                print("Error: Player 1 has no stones left to place.")
                successful_move = False
            elif current_player == 2 and player2_stone_reserves == 0:
                print("Error: Player 2 has no stones left to place.")
                successful_move = False
            else:
                place_stone(board, current_player, standing=True)

            # Logic for first 2 moves, and passing to the next player
            if successful_move:
                if not playing_against_AI:
                    current_player = 2 if current_player == 1 else 1
                if first_moves[0]:
                    first_moves = (False, first_moves[1])

        case "move":
            if not first_moves[0] == first_moves[1] == False:
                print("Error: You cannot move a stack until the first 2 moves have been made.")
                successful_move = False
            if not player_has_movable_stack(board,current_player):
                print("Error: You have no movable stacks on the board, please select another action.")
                successful_move = False

            InvalidInput = True
            while InvalidInput:
                row, col = select_square(board)
                current_stack = board[row][col]
                if len(current_stack) == 1:
                    print(f"Error: There is no stack to move at row {row+1}, column {alpha[col]}. Please select another position.")
                elif (current_player+1) not in current_stack:
                    print(f"Error: Player {current_player} does not own the stack at row {row+1}, column {alpha[col]}.")
                else:
                    InvalidInput = False
            move_stack(board, current_player, row, col)

            if not playing_against_AI and successful_move:
                current_player = 2 if current_player == 1 else 1
        case "exit":
            print("Exiting the game.")
            return -1
        case _:
            print("Sorry, that is not a valid move.")
            print("type \"help\" for more info")
            successful_move = False
    
    print_board(board)
    
    if not successful_move:
        exit_game = game_loop(board, current_player) # Restart here if the move was unsuccessful
        if exit_game == -1:
            return -1

    if playing_against_AI:
        # Check game ending conditions and stalemate:
        win, winner, path = check_win_conditions(board, opponentAI, player2_stone_reserves)
        if win:
            if len(path) == 0:
                print(f"Winner is player {winner-1} via flats differential!")
            else:
                startPath = path[0]
                endPath = path[-1]
                start = (startPath[0]+1, alpha[startPath[1]])
                end = (endPath[0]+1, alpha[endPath[1]])
                print(f"Winner is player {winner-1} via path from {start} to {end}!")
            return winner-1
        if not player_has_movable_stack(board, 2) or opponent_stones_left <= 0:
            print("The game has ended in a stalemate!")
            return 0
        
        ################# AI shenanigans #################
        print("AI is thinking...")
        board_copy = copy.deepcopy(board)
        if first_moves[1]:
            """ action = GameAI.iterative_deepening_worst(board_copy, current_player, opponentAI, player1_stone_reserves, player2_stone_reserves, 4, False, transposition_table, time_limit=20) """
            action = GameAI.AI_first_move(board, current_player, opponentAI, player1_stone_reserves, player2_stone_reserves)
            print('BOARD PRINT: ', board)
            print(action)
            first_moves = (first_moves[0], False)
            print("AI found bad action.")
            apply_action(board, action, current_player)
        else:
            action = GameAI.iterative_deepening(board_copy, opponentAI, current_player, player2_stone_reserves, player1_stone_reserves, 4, True, transposition_table, time_limit=20)
            print("AI found good action.")
            apply_action(board, action, opponentAI)

        print(f"AI {action[0]} row:{action[1]+1} col:{alpha[action[2]]}.")
        print_board(board)
        ############## AI shenanigans done ###############

    #Check game ending conditions and stalemate:
    win, winner, path = check_win_conditions(board, current_player, stones_left)
    if not win:
        if player_has_movable_stack(board, current_player) or opponent_stones_left > 0:
            game_loop(board, current_player)
        else:
            print("The game has ended in a stalemate!")
            return 0
    else:
        if len(path) == 0:
            print(f"Winner is player {winner-1} via flats differential!")
        else:
            startPath = path[0]
            endPath = path[-1]
            start = (startPath[0]+1, alpha[startPath[1]])
            end = (endPath[0]+1, alpha[endPath[1]])
            print(f"Winner is player {winner-1} via path from {start} to {end}!")
        return winner

if __name__ == "__main__":
    board = None

    if len(sys.argv) != 2:
        print_usage(sys.argv[0])
        exit()

    try:
        if not has_txt_format(sys.argv[1]):
            raise ValueError
        # Read the board from a file given in arguments
        board = read_board(sys.argv[1])
    except FileNotFoundError or ValueError:
        print("Error: File is not a valid board.")
        exit()
    
    human_or_AI = None
    while human_or_AI not in ['a', 'h','human', 'ai']:
        human_or_AI = input('Play versus human or AI?: ').strip().lower()
        if human_or_AI not in ['a', 'h','human', 'ai']:
            print("Error: Invalid input. Please enter human or AI.")

    if human_or_AI == 'ai' or human_or_AI == 'a':
        playing_against_AI = True

    print("Starting board:")
    print_board(board)
    
    # Deactivate the first moves logics if the board is not empty at start
    # NOTE: It is impossible to determine which players turn it is if the board is not empty at start. 
    # In our solution, we always let Player 1 start.
    initial_amount = player1_stone_reserves
    player1_stone_reserves, player2_stone_reserves = evaluation.pieces_left(board, player1_stone_reserves, player2_stone_reserves)
    if player2_stone_reserves < initial_amount:
        first_moves = (False, first_moves[1])
    if player1_stone_reserves < initial_amount:
        first_moves = (first_moves[0], False)

    # Start the game loop
    if not check_win_conditions(board, 1, player1_stone_reserves)[0] and not check_win_conditions(board, 2, player2_stone_reserves)[0]:
        winner = game_loop(board, current_player)
    else:
        print("The game has ended before it started.")
        exit()
    
    save_transposition_table(transposition_table)
    if winner != -1:
        # Ask if we want to save the board
        answer = None
        while answer not in ['y', 'yes', 'n', 'no']:
            answer = input('Do you want to save the finished board? (y/yes/n/no): ').strip().lower()
            if answer not in ['y', 'yes', 'n', 'no']:
                print('Invalid input. Try again.')
        if answer not in ['n','no']:
            save_board_name = None
            while not has_txt_format(save_board_name):
                save_board_name = input('Please enter a valid filename to save. Must end in \'.txt\': ').strip().lower()
                if not has_txt_format(save_board_name):
                    print('Invalid input. Try again.')
            write_board(save_board_name, board)
            print(f"Board saved as {save_board_name}")
    print("Game exited successfully.")