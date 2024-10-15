from collections import deque
import time

"""
This file contains the implementation of the BFS algorithm to find the best path to the opposite side of the board
* The board is represented as a 2D list of lists
* threat_assessment() function is used to evaluate the board and calculate the threat level score for a player
"""

def get_valid_edge_pieces(board):
    """
    Function to get the valid edge pieces of the board
    * A valid edge piece is a piece that is not standing and is on the edge of the board
    """
    
    edge_pieces = []
    for row in range(len(board)):
        for col in range(len(board[row])):
             
            #  Check if the piece is not standing and is on the edge of the board
             if (row == 0 or row == len(board) - 1 or col == 0 or col == len(board[row]) - 1) and board[row][col][0] != 1:
                edge_pieces.append((row, col))
    return edge_pieces



# Helper functions for BFS algorithm

def define_finish_edges(row, col, rows, cols):
    finish_edges = []

    if col == 0:
        finish_edges.extend([(i, cols - 1) for i in range(rows)]) # Right edge
    
    if col == cols - 1:
        finish_edges.extend([(i, 0) for i in range(rows)])  # Left edge
        
    if row == 0:
        finish_edges.extend([(rows - 1, i) for i in range(cols)])  # Bottom edge
        
    if row == rows - 1:
        finish_edges.extend([(0 , i) for i in range(cols)])  # Top edge

    return finish_edges




def bfs_find_paths(start, board, finish_edges):
    """
    Function to find the paths from a given start piece to the opposite side of the board
    * The start piece must be on the edge of the board
    * The function uses a breadth-first search to find all possible paths
    * Returns a list of paths to the opposite side of the board
    """

    rows, cols = len(board), len(board[0])
    start_row, start_col = start

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


    # Initialize the BFS queue with the start position
    queue = deque([(start_row, start_col, None)])
    visited = set([(start_row, start_col)])


    parent_map = {}
    paths = []

    while queue: 
        row, col, parent = queue.popleft()
        parent_map[(row, col)] = parent
        # Check if the current position is a boundary, if it is, add the path to the list
        if (row, col) in finish_edges:
            paths.append(reconstruct_path((row, col), parent_map))
            continue
            

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # Check if the new position is within the grid and not visited
            if 0 <= new_row < rows and 0 <= new_col < cols and (new_row, new_col) not in visited:

                # If next piece is standing, skip
                if board[new_row][new_col][0] == 1:
                    continue

                visited.add((new_row, new_col))
                queue.append((new_row, new_col, (row, col)))

    return paths

def reconstruct_path(node, parent_map):
    """
    Helper function to reconstruct a path from the finish node to the start using parent pointers.
    """
    path = []
    while node is not None:
        path.append(node)
        node = parent_map[node]
    return path[::-1] 

def find_best_path(paths, board):
    """
    Function to find the best path from a list of paths
    * The best path is the path with the least number of pieces that are not the player's
    * Eg. [[[0,2], [0,2], [0,2], [0]],
          [[0],    [0],   [0],   [0]],
          [[0],    [0],   [0],   [0]],
          [[0],    [0],   [0],   [0]]]
          Will return 1, 4 as there is just one piece that needs to be placed for p1 and 4 for p2
    """



    players = [2, 3]

    player_one_min_path_length = float('inf')
    player_two_min_path_length = float('inf')

    for path in paths: 
        p1_pieces = 0
        p2_pieces = 0
        for (row, col) in path:
            if board[row][col][-1] == players[0]:
                p1_pieces += 1
            elif board[row][col][-1] == players[1]:
                p2_pieces += 1
                
        p1_pieces_left = len(path) - p1_pieces
        p2_pieces_left = len(path) - p2_pieces

        if p1_pieces_left < player_one_min_path_length:
            player_one_min_path_length = p1_pieces_left

        if p2_pieces_left < player_two_min_path_length:
            player_two_min_path_length = p2_pieces_left

    return player_one_min_path_length, player_two_min_path_length



def evaluate_board_paths(board):
    """
    Function to evaluate the board and find the best path to the opposite side of the board.
    * The function uses the BFS algorithm to find all possible paths from the edge pieces of the board.
    * The function then finds the best path from the list of paths.
    * The best path is the path with the least number of pieces that are not the player's.
    * Returns the piece(s) that need to be placed to get to the opposite side of the board.
    * Returns None if no path is found for a player.
    """
    
    edge_pieces = get_valid_edge_pieces(board)
    p1_best_pieces_left = float('inf')
    p2_best_pieces_left = float('inf')
    p1_path_found = False
    p2_path_found = False
    
    for piece in edge_pieces:
        finish_edges = define_finish_edges(piece[0], piece[1], len(board), len(board))
        paths = bfs_find_paths(piece, board, finish_edges)

        if not paths:
            continue

        p1_pieces_left, p2_pieces_left = find_best_path(paths, board)        

        if p1_pieces_left < p1_best_pieces_left:
            p1_best_pieces_left = p1_pieces_left
            p1_path_found = True
            
        if p2_pieces_left < p2_best_pieces_left:
            p2_best_pieces_left = p2_pieces_left
            p2_path_found = True

    # Check if any path was found for player 1 or player 2 after all edge pieces are processed
    if not p1_path_found:
        p1_best_pieces_left = None  

    if not p2_path_found:
        p2_best_pieces_left = None

    return p1_best_pieces_left, p2_best_pieces_left


def threat_assessment(board):
    """
    Returns the score for the players threat level
    * High score = close to winning, low score = far from winning
    * If a player is more than 4 pieces away from winning, the score is 0
    * Returns -1 if no path is found
    * Returns 0 if the player has already won
    * TODO: Run function for both players and return a tuple of scores
    """

    p1_pieces_left, p2_pieces_left = evaluate_board_paths(board) 
    score_mapping_p1 = {4: -1, 3: -10, 2: -1000, 1: -100000, 0: float('-inf')} 
    score_mapping_p2 = {4: -1, 3: -10, 2: -1000, 1: -100000, 0: float('-inf')} 

    if p1_pieces_left is None:
        p1_score = 0
    else:
        p1_pieces_left = min(p1_pieces_left, 4)
        p1_score = score_mapping_p1.get(p1_pieces_left, 0)

    if p2_pieces_left is None:
        p2_score = 0
    else:
        p2_pieces_left = min(p2_pieces_left, 4)
        p2_score = score_mapping_p2.get(p2_pieces_left, 0)

    return p1_score, p2_score



    
    

# Test the functions
empty_board =  [[[0,3], [1,2], [0,2], [0,3]],
                 [[1], [1,2], [1], [1]],
                 [[0], [0], [0], [1]],
                 [[0], [1], [0], [0]]]


example_board = [[[1, 2],       [0, 3, 2],     [1, 3,2],    [1,3]],
                 [[0, 2, 2],     [1, 3, 2],  [0, 3],    [0, 2, 3]],
                 [[1, 3],        [0, 2],     [0, 2], [1, 3, 2, 3]],
                 [[0, 3, 2],     [0, 2],  [1, 3],       [0, 3, 2, 3]]]


# start = time.time()
# # for i in range(130000): 
# #     threat_assessment(example_board, 2)

# # print("Time taken: ", time.time() - start)
# for i in range(1300):
#     threat_assessment(empty_board, 2)
# start = time.time()

# for i in range(130000):
#     p1, p2 = threat_assessment(empty_board)    

# print(p1, p2)
# print("Time taken: ", time.time() - start)
# print(threat_assessment(empty_board))
# TODO: Implement a break when finding a path with 1 pieces left