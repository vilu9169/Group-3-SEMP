board_size = 4

def generate_placement_moves(board, player, player_reserves):
    moves = []
    
    if player_reserves > 0:
        for row in range(board_size):
            for col in range(board_size):
                if board[row][col][0] == 0: # top piece is flat
                    moves.append(['lay', row, col])
                    moves.append(['stand', row, col])
    return moves

def available_directions(row, col):
    directions = {}
    if row != 0: 
        directions['up'] = (-1, 0, row)
    if row != board_size-1:
        directions['down'] = (1, 0, board_size - 1 - row)
    if col != 0:
        directions['left'] = (0, -1, col)
    if col != board_size-1:
        directions['right'] = (0, 1, board_size - 1 - col) 

    return directions

def find_all_player_stacks(board, player):
    stacks = [] # [row, col, start, stacked_flats]
    # Iterate through board
    for row in range(board_size):
        for col in range(board_size):
            # Only proceed if player has flat in stack
            if player+1 in board[row][col]:
                stack = board[row][col]
                # Disregard last if piece is standing
                #if board[row][col][0] == 1:
                    #stack = board[row][col][:-1]
                #else:
                    #stack = board[row][col]
                # Find all personal stacks in big stack
                for index, flat in enumerate(stack):
                    # Keep track of stacked flats
                    stacked_flats = 0
                    # Find flat belonging to player
                    if flat == player+1:
                        # Save start index
                        start = index
                        stacked_flats += 1
                        # Find all stacked flats
                        while(index+1 < len(stack) and stack[index+1] == player+1):
                            stacked_flats += 1
                            index += 1
                        stacks.append([row, col, start, stacked_flats])
    return stacks


def generate_drop_sequences(total_flats, max_steps):
    sequences = []

    def helper(remaining_flats, steps_left, current_sequence):
        if steps_left == 0:
            if remaining_flats == 0:
                sequences.append(current_sequence)
            return
        if remaining_flats < steps_left:
            return  # Not enough stones to continue
        min_drop = 1
        max_drop = remaining_flats - (steps_left - 1)  # Ensure at least 1 stone per remaining step
        for drop_count in range(min_drop, max_drop + 1):
            helper(
                remaining_flats - drop_count,
                steps_left - 1,
                current_sequence + [drop_count]
            )
                
    max_possible_steps = min(total_flats, max_steps)
    for steps in range(1, max_possible_steps + 1):  # Adjusted range
        helper(total_flats, steps, [])

    return sequences


def generate_stack_moves(board, player):
    stacks = find_all_player_stacks(board, player)
    moves = []
    for stack in stacks:
        row = stack[0]
        col = stack[1]
        start = stack[2]
        stacked_flats = stack[3]
        directions = available_directions(row, col)
        for direction in directions.keys():
            for i in range(directions[direction][2]):
                row_move = directions[direction][0] * (i+1)
                col_move = directions[direction][1] * (i+1)
                if board[row + row_move][col + col_move][0] == 1:
                    break
            else:
                standing = board[row][col][0] == 1
                drop_sequences = generate_drop_sequences(stacked_flats, directions[direction][2])
                for sequence in drop_sequences:
                    moves.append(['move', row, col, start, direction, sequence, standing])
            continue
            
        
    return moves

def generate_stack_moves_old(board, player):
    moves = []
    for row in range(board_size):
            for col in range(board_size):
                if player+1 in board[row][col] and board[row][col][1] == player+1:
                    directions = available_directions(row, col)
                    for direction in directions.keys():
                        for i in range(directions[direction][2]):
                            row_move = directions[direction][0] * i
                            col_move = directions[direction][1] * i
                            if board[row + row_move][col + col_move][0] == 1:
                                break
                            else:
                                moves.append(['move', row, col, direction, i])
    return moves

def generate_moves(board, player, player_reserves):
    moves = []
    moves += generate_placement_moves(board, player, player_reserves)
    moves += generate_stack_moves(board, player)
    return moves