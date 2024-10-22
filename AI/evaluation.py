from collections import deque
import AI.board as GameLogic

board = [
    [[1, 2]   , [0, 3]   , [1, 3, 2], [0]],
    [[0, 2, 2], [1, 3, 3], [0, 3, 2], [0, 2, 2]],
    [[1, 3, 2], [0, 2], [0, 2, 2, 2], [0, 3, 2]],
    [[1, 3, 2], [1, 2, 3], [0, 3, 2], [1, 3, 2]]
]

empty_board = [
    [[1,2], [0], [0], [0,2]],
    [[0], [0], [0], [0]],
    [[0], [0], [0], [0]],
    [[0], [0], [0], [0,2]]
]

def generate_possible_placements(board):
    # Function that generates all possible moves for a given player
    # A "move" is the coordinates for where a placement is possible
    n = len(board)
    moves = []

    for i in range(n):
        for j in range(n):
            pos = board[i][j]
            if pos[0] == 1:
                continue
            moves.append([i, j])

    return moves


# def generate_controlled_stacks(board, player):
#     """
#     Generate all controlled stacks for a given player.
#     * A controlled stack is a stack where the top piece is the players piece.  
#     * Can be used for win
#     """
#     n = len(board)
    
#     controlled_stacks = []
#     moves = []


#     for i in range(n):
#         for j in range(n):
#             pos = board[i][j]

#             # Check if the stack is controlled by the player, and top piece is flat
#             if pos[-1] != player or len(pos) < 3 or pos[0] == 1:
#                 continue
            
#             controlled_stacks.append([i, j])

#     return controlled_stacks

# def generate_movable_stacks(board, player):
#     n = len(board)
#     movable_stacks = []

#     for i in range(n):
#         for j in range(n):
#             pos = board[i][j]
#             if len(pos) < 2:
#                 continue

#             # Check if the stack is controlled by the player, and top piece is flat
#             if pos[1] != player or pos[0] == 1:
#                 continue
            
#             movable_stacks.append([i, j])

#     return movable_stacks


# def generate_stack_moves(board, player):

#     # TODO Implement this function
#     n = len(board)
#     # controlled_stacks = generate_controlled_stacks(board, player)
#     movable_stacks =  generate_movable_stacks(board, player)


#     for pos in movable_stacks:
#         # Stack is defined as a list of coordinates
#         i, j = pos
#         stack = board[i][j]
#         nr_of_moves = 0


#         # Check if the stack can move in any direction
#         # and calculate the number of moves possible
#         for piece in stack[1:]:
#             if piece == player:
#                 nr_of_moves += 1
#             else: 
#                 break

#     return None  

def flats_differential(board, player, opponent):
    """
    Calculate the number of flats on the board contra the opponent.
    * Returns the difference between the number of flats for the player and the opponent.
    """

    n = len(board)
    flats = 0
    opponent_flats = 0

    for i in range(n):
        for j in range(n):
            pos = board[i][j]
            if pos[-1] == player+1 and pos[0] == 0:
                flats += pos.count(player+1)
            elif pos[-1] != player+1 and pos[0] == 0:
                opponent_flats += pos.count(opponent+1)

    return flats - opponent_flats

def stack_strength(board, player):
    """
    Estimate the strength of placed stacks of flats.
    * top belonging to the player.
    * Total flats belonging to the player.
    * Possible mobility and positioning of stack.
    * max antal sammanhängande flats

    return a 2D list containing lists that contain the corrdinates and the strenght of the stack
    [[x, y, strength], [x, y, strength] .....
    """
    stacks_strengths = 0
    
    n = len(board)
    for i in range(n):
        for j in range(n):
            strength = 0
            flats = 0
            possible_direction = 0
            top = 0
            temp = 0
            max_flats = 0 
            if len(board[i][j])<2: #checks empty space
                stacks_strengths += 0
            else:
                if board[i][j][-1] == player + 1: #checks top
                    top += 1
                if (board[i][j][1] == player + 1): #checks top for flats
                    if (board[i][j][0] == 0):
                        flats += 1
                    temp += 1
                    max_flats += 1
                for k in range(2,len(board[i][j])): #skips top stone and counts rest of the stack
                    if (board[i][j][k] == player + 1):
                        flats += 1
                        temp += 1
                        max_flats = max(max_flats, temp)
                    else: 
                        max_flats = max(max_flats, temp)
                        temp = 0
                if (i < 3 and board[i+1][j][0] == 0):
                    possible_direction += 1  
                if (i > 0 and board[i-1][j][0] == 0):
                    possible_direction += 1 
                if (j < 3 and board[i][j+1][0] == 0):
                    possible_direction += 1 
                if (j > 0 and board[i][j-1][0] == 0):
                    possible_direction += 1   
                #print("flats = " + str(flats) + ", possible_direction = " + str(possible_direction) + ", top = " + str(top) + ", maxflats= " + str(max_flats))
                if flats == 0 and top == 0:
                    possible_direction = 0
                strength = flats + possible_direction + top + max_flats
                stacks_strengths += strength
    
    return stacks_strengths
                
def test_stack_strength():
    # Test case 1: Empty board (all positions are empty)
    board_emp = [
        [[0], [0], [0], [0]],
        [[0], [0], [0], [0]],
        [[0], [0], [0], [0]],
        [[0], [0], [0], [0]]
    ]
    player = 1  # Red (Player 1)
    expected_empty = [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0],
                      [1, 0, 0], [1, 1, 0], [1, 2, 0], [1, 3, 0],
                      [2, 0, 0], [2, 1, 0], [2, 2, 0], [2, 3, 0],
                      [3, 0, 0], [3, 1, 0], [3, 2, 0], [3, 3, 0]]
    
    assert stack_strength(board_emp, player) == expected_empty, "Test 1 failed: Empty board test"

    # Test case 2: Single flat stone for the player (lying stone)
    board_single_flat = [
        [[0], [0], [0], [0]],
        [[0], [0, 2], [0], [0]],  # Red (Player 1) lying stone at (1,1)
        [[0], [0], [0], [0]],
        [[0], [0], [0], [0]]
    ]
    expected_single_flat = [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0],
                            [1, 0, 0], [1, 1, 7], [1, 2, 0], [1, 3, 0],
                            [2, 0, 0], [2, 1, 0], [2, 2, 0], [2, 3, 0],
                            [3, 0, 0], [3, 1, 0], [3, 2, 0], [3, 3, 0]]
    assert stack_strength(board_single_flat, player) == expected_single_flat, "Test 2 failed: Single flat stone test"

    # Test case 3: Single standing stone for another player (blocking)
    board_single_standing = [
        [[0], [0], [0], [0]],
        [[0], [1, 3], [0], [0]],  # Blue (Player 2) standing stone at (1,1)
        [[0], [0], [0], [0]],
        [[0], [0], [0], [0]]
    ]
    expected_single_standing = [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0],
                                [1, 0, 0], [1, 1, 0], [1, 2, 0], [1, 3, 0],
                                [2, 0, 0], [2, 1, 0], [2, 2, 0], [2, 3, 0],
                                [3, 0, 0], [3, 1, 0], [3, 2, 0], [3, 3, 0]]
    
    assert stack_strength(board_single_standing, player) == expected_single_standing, "Test 3 failed: Standing stone test"

    # Test case 4: Mixed stack (lying and standing stones) with mobility test
    board_mixed_stack = [
        [[0], [0], [0], [0]],
        [[0], [1, 2, 3, 2], [0], [0]],  # Red (Player 1) standing stone on top, with lying stones below at (1,1)
        [[0], [0], [0], [0]],
        [[0], [0], [0], [0]]
    ]
    expected_mixed_stack = [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0],
                            [1, 0, 0], [1, 1, 7], [1, 2, 0], [1, 3, 0],
                            [2, 0, 0], [2, 1, 0], [2, 2, 0], [2, 3, 0],
                            [3, 0, 0], [3, 1, 0], [3, 2, 0], [3, 3, 0]]
    #print(stack_strength(board_mixed_stack, 1))

    assert stack_strength(board_mixed_stack, player) == expected_mixed_stack, "Test 4 failed: Mixed stack test"

    #print("All tests passed!")

# Run the test function
#test_stack_strength()

def test_stack_strength_multiple():
    # Test case 5: More complex scenario with multiple stacks
    board_complex = [
        [[0], [0, 2], [0, 3], [0]],  # Red lying stone (0,1), Blue lying stone (0,2)
        [[0], [1, 3, 2, 2], [0], [0]],  # Blue standing stone on top at (1,1) with Red lying below
        [[0], [0, 3, 2], [1, 2], [0]],  # Mixed stack at (2,1), Standing Red stone at (2,2)
        [[0], [0], [0], [0]]
    ]
    player = 1  # Red (Player 1)
    expected_complex = [[0, 0, 0], [0, 1, 5], [0, 2, 0], [0, 3, 0],
                        [1, 0, 0], [1, 1, 9], [1, 2, 0], [1, 3, 0],
                        [2, 0, 0], [2, 1, 5], [2, 2, 6], [2, 3, 0],
                        [3, 0, 0], [3, 1, 0], [3, 2, 0], [3, 3, 0]]
    assert stack_strength(board_complex, player) == expected_complex, "Test 5 failed: Complex board test"

    # Test case 6: Board with mixed blocking and open areas
    board_mixed = [
        [[0], [0], [0], [0]],
        [[0], [1, 2], [0, 3], [0]],  # Standing Red stone at (1,1), Lying Blue stone at (1,2)
        [[0], [0], [0], [1, 2]],  # Standing Red stone at (2,3)
        [[0], [0], [0], [0]]
    ]
    expected_mixed = [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0],
                      [1, 0, 0], [1, 1, 6], [1, 2, 0], [1, 3, 0],
                      [2, 0, 0], [2, 1, 0], [2, 2, 0], [2, 3, 5],
                      [3, 0, 0], [3, 1, 0], [3, 2, 0], [3, 3, 0]]
    assert stack_strength(board_mixed, player) == expected_mixed, "Test 6 failed: Mixed blocking test"

    # Test case 7: Board with alternating lying stones
    board_alternating = [
        [[0, 2], [1, 3], [0, 2], [0, 3]],  # Alternating Red and Blue lying stones in row 0
        [[0], [0], [0], [0]],
        [[0], [0], [0], [0]],
        [[0], [0], [0], [0]]
    ]
    expected_alternating = [[0, 0, 4], [0, 1, 0], [0, 2, 5], [0, 3, 0],
                            [1, 0, 0], [1, 1, 0], [1, 2, 0], [1, 3, 0],
                            [2, 0, 0], [2, 1, 0], [2, 2, 0], [2, 3, 0],
                            [3, 0, 0], [3, 1, 0], [3, 2, 0], [3, 3, 0]]
    #print(stack_strength(board_alternating, 1))
    assert stack_strength(board_alternating, player) == expected_alternating, "Test 7 failed: Alternating stones test"

    # Test case 8: Board with multiple layers of lying stones
    board_multiple_layers = [
        [[0], [0], [0], [0]],
        [[0], [1, 2, 3, 2, 3, 2], [0], [0]],  # Multiple layers of Red lying stones with one standing on top at (1,1)
        [[0], [0], [0], [0]],
        [[0], [0], [0], [0]]
    ]
    expected_multiple_layers = [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0],
                                [1, 0, 0], [1, 1, 8], [1, 2, 0], [1, 3, 0],
                                [2, 0, 0], [2, 1, 0], [2, 2, 0], [2, 3, 0],
                                [3, 0, 0], [3, 1, 0], [3, 2, 0], [3, 3, 0]]
    assert stack_strength(board_multiple_layers, player) == expected_multiple_layers, "Test 8 failed: Multiple layers test"

    #print("All tests passed in test_stack_strength_multiple!")

# Run test function
#test_stack_strength_multiple()

def pieces_left(board, player1_stones, player2_stones):
    """
    Number of available pieces not yet placed for one player contra the other.
    * Larger amount more powerful.
    """
    n = len(board)

    for i in range(n):
        for j in range(n):
            pos = board[i][j]
            player1_stones -= pos.count(2)
            player2_stones -= pos.count(3)

    return player1_stones, player2_stones

def board_control(board, player):
    """
    Estimate the control a player has over the board.
    * Evaluate placement of pieces. 
    """

    rows, cols = len(board), len(board[0])

    control_score = 0

    for i in range(rows):
        for j in range(cols):
            pos = board[i][j]
            if not pos:
                continue
            
            blocked = False
            for row in range(rows):
                if board[row][j][0] == 1:
                    blocked = True
            for col in range(cols):
                if board[i][col][0] == 1:
                    blocked = True

            if blocked == True:
                control_score -= 5
            top_piece = pos[-1]

            if top_piece == player+1:
                if pos[0] == 0:
                    # Top is flat
                    control_score += 1

                if pos[0] == 1:
                    # Top is standing
                    control_score += 1

                if 1 <= i < rows - 1 and 1 <= j < cols - 1:
                    # Piece is in the middle 2x2 area
                    control_score += 1

                if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
                    # Piece is on the edge
                    control_score += 0.5

    return control_score    

def pieces_left(board, player1_stones, player2_stones):
    """
    Number of available pieces not yet placed for one player contra the other.
    * Larger amount more powerful.
    """
    n = len(board)

    for i in range(n):
        for j in range(n):
            pos = board[i][j]
            player1_stones -= pos.count(2)
            player2_stones -= pos.count(3)

    return player1_stones, player2_stones


def controlled_pieces(board, player):
    """
    Number of controlled pieces for one player.
    * More controlled pieces more powerful.
    """
    n = len(board)
    controlled = 0

    for i in range(n):
        for j in range(n):
            pos = board[i][j]
            if pos[-1] == player+1:
                controlled += 1
            elif len(pos) > 1:
                controlled -= 1
    return controlled

def road_strength(board, player):
    """
    Estimate the strength of the placed roads for one player.
    * Returns the length of the longest road.
    """

    rows, cols = len(board), len(board[0])

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    visited = [[False for _ in range(cols)] for _ in range(rows)]

    def bfs(start_row, start_col):
        """
        Perform BFS to find the length of the connected path.
        """
        queue = deque([(start_row, start_col)])
        visited[start_row][start_col] = True
        path_length = 1
        longest_path = [(start_row, start_col)]

        while queue:
            row, col = queue.popleft()

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc

                if 0 <= new_row < rows and 0 <= new_col < cols and not visited[new_row][new_col]:
            
                    # Check if the new cell belongs to the same player and is not a blocked piece
                    if board[new_row][new_col][-1] == player+1 and board[new_row][new_col][0] != 1:
                        visited[new_row][new_col] = True
                        queue.append((new_row, new_col))
                        path_length += 1 
                        longest_path.append((new_row, new_col))

                    elif board[new_row][new_col][0] == 0:
                        
                        if (new_row + 1) < rows and not visited[new_row + 1][new_col] and (board[new_row + 1][new_col][-1] == player +1) and (board[new_row + 1][new_col][0] != 1):
                            longest_path.append((new_row +1, new_col))
                        if (new_row - 1) >= 0 and not visited[new_row - 1][new_col] and (board[new_row - 1][new_col][-1] == player +1) and (board[new_row - 1][new_col][0] != 1):
                            longest_path.append((new_row -1, new_col))
                        if (new_col + 1) < cols and not visited[new_row][new_col + 1] and (board[new_row][new_col +1][-1] == player +1) and (board[new_row][new_col + 1][0] != 1):
                            longest_path.append((new_row, new_col + 1))
                        if (new_col - 1) >= 0 and not visited[new_row][new_col - 1] and (board[new_row][new_col -1][-1] == player +1) and (board[new_row][new_col - 1][0] != 1):
                            longest_path.append((new_row, new_col-1))
        # print("len" +str(len(longest_path)))
        return longest_path
    potential = road_potential(board, player)
    longest_road = 0
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and board[i][j][-1] == player+1 and board[i][j][0] != 1:
                path = bfs(i, j)
                if len(path) > 1:
                    longest_road += len(path)

    return longest_road + potential


def road_potential(board, player):
    
    controlled_pieces_in_rows = 0
    controlled_pieces_in_cols = 0

    # Check each row for potential roads
    for row in range(len(board)):
        controlled_pieces_in_row = 0
        standing_found_row = False
        for col in range(len(board[row])):
            if board[row][col][0] == 1:
                standing_found_row = True
            if board[row][col][-1] == player + 1:
                controlled_pieces_in_row += 1
        
        if not standing_found_row:
            controlled_pieces_in_rows += controlled_pieces_in_row

    # Check each column for potential roads
    for col in range(len(board[0])):
        controlled_pieces_in_col = 0
        standing_found_col = False
        for row in range(len(board)):
            if board[row][col][0] == 1:
                standing_found_col = True
            if board[row][col][-1] == player + 1:
                controlled_pieces_in_col += 1

        if not standing_found_col:
            controlled_pieces_in_cols += controlled_pieces_in_col
    
    if controlled_pieces_in_rows < 2:
        controlled_pieces_in_rows = 0
    
    if controlled_pieces_in_cols < 2:
        controlled_pieces_in_cols = 0

    return (controlled_pieces_in_rows + controlled_pieces_in_cols) * 0.5


    





# def available_pieces(board, AI, player):
#     """
#     Number of available pieces not yet placed for AI contra the player.
#     * Larger amount more powerful.
#     """

#     n = len(board)
#     AI_pieces = 0
#     player_pieces = 0

#     for i in range(n):
#         for j in range(n):
#             pos = board[i][j]
#             AI_pieces += pos.count(AI)
#             player_pieces += pos.count(player)

#     return AI_pieces - player_pieces



def count_adjacent_opponent_pieces(board, position, player):
    """
    Counts amount of adjacent flat pieces that belongs to the opponent.
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    pieces = 0
    n = len(board)
    row = position[0]
    col = position[1]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc

        # Check if the new position is within the grid and not visited
        if 0 <= new_row < n and 0 <= new_col < n:
            new_pos = board[new_row][new_col]
            if (len(new_pos) > 1 and new_pos[-1] != player+1 and new_pos[0] != 1):
                pieces += 1

    return pieces


def blocking_potential(board, player):
    """
    Should return the position with the most blocking potential
    Takes a square in the board and counts the amount of adjacent pieces where
    the top piece belongs to the other player.

    This function is wonky when theres few pieces on the board.
    Maybe possible to tweak weight when there's more pieces on the board?
    """
    moves = generate_possible_placements(board)
    best_move = 0 # Default best move. TODO: What happens when moves is empty?
    highest_block_score = 0
    for move in moves:
        block_score = count_adjacent_opponent_pieces(board, move, player)
        if block_score > highest_block_score:
            highest_block_score = block_score
            best_move = block_score
    return best_move


# TODO: Implement the following functions
# - board_control

# TODO: Clean up code and remove unused functions


#print(road_strength(empty_board,1))