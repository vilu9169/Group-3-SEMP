import time
import AI.board as GameLogic
import AI.MoveGenerator as MoveGenerator
import AI.evaluation as evaluation
import AI.threat_assessment_2p as threat_assessment
import copy
import pickle
import os

weights = {
    'road_strength': 150,
    'flats_differential': 100,
    'blocking_potential': 5,
    'stack_strength': 1,
    'board_control': 10,
    'available_pieces': 10,
    'controlled_pieces': 100,
    'threat_assessment': 1 # Threat assessment is -INF
}

def evaluate(board, player, opponent):
    """
    Wrapper for the different evaluation metrics.
    """
    max_values = {
        'road_strength': 9,  # Max possible road length
        'flats_differential': 15,  # Max flats difference
        'blocking_potential': 4,  # Max blocking potential in a position
        'stack_strength': 35,  # An estimated max value
        'board_control': 17,  # Max control of the board
        'available_pieces': 14,  # Max difference in available pieces
        'controlled_pieces': len(board) * len(board[0]),  # Max number of controlled pieces
        'threat_assessment': 1,  # Since it returns -inf when a threat is detected
    }
    
    score = 0
    road_strength_good = evaluation.road_strength(board, player)
    road_strength_bad = evaluation.road_strength(board, opponent)
    if road_strength_good > 1 or road_strength_bad > 1:
        threat = threat_assessment.threat_assessment(board)
        threat_score = threat[0] + threat[1] * -1
        score += threat_score
    score += road_strength_good * weights['road_strength'] / max_values['road_strength']
    score += evaluation.flats_differential(board, player, opponent) * weights['flats_differential'] / max_values['flats_differential']
    score += evaluation.controlled_pieces(board, player) * weights['controlled_pieces'] / max_values['controlled_pieces']
    score += evaluation.blocking_potential(board, player) * weights['blocking_potential'] / max_values['blocking_potential']
    score += evaluation.stack_strength(board, player) * weights['stack_strength'] / max_values['stack_strength']
    score += evaluation.board_control(board, player) * weights['board_control'] / max_values['board_control']

    """print("-----------NEW EVALUATION-------------")
    GameLogic.print_board(board)
    print(player)
    print(f"Road strength: {evaluation.road_strength(board, player) * weights['road_strength'] / max_values['road_strength']}")
    print(f"Threat assessment: {threat_assessment.threat_assessment(board)}")
    print(f"Flats differential: {evaluation.flats_differential(board, player, opponent) * weights['flats_differential'] / max_values['flats_differential']}")
    #print(f"Available pieces: {evaluation.available_pieces(board, player, opponent) * weights['available_pieces'] / max_values['available_pieces']}")
    print(f"Controlled pieces: {evaluation.controlled_pieces(board, player) * weights['controlled_pieces'] / max_values['controlled_pieces']}")
    print(f"Blocking potential: {evaluation.blocking_potential(board, player) * weights['blocking_potential'] / max_values['blocking_potential']}")
    print(f"Stack strenth: {evaluation.stack_strength(board, player) * weights['stack_strength'] / max_values['stack_strength']}")
    print(f"Board Control: {evaluation.board_control(board, player) * weights['board_control'] / max_values['board_control']}")
    print(f"Eval score is: {score}")
    print("-----------END EVALUATION-------------")#"""
    return score


def evaluate_sort(board, player, opponent):
    """
    Wrapper for the different evaluation metrics.
    """
    max_values = {
        'road_strength': 9,  # Max possible road length
        'flats_differential': 15,  # Max flats difference
        'blocking_potential': 4,  # Max blocking potential in a position
        'stack_strength': 35,  # An estimated max value
        'board_control': 17,  # Max control of the board
        'available_pieces': 14,  # Max difference in available pieces
        'controlled_pieces': len(board) * len(board[0]),  # Max number of controlled pieces
        'threat_assessment': 1,  # Since it returns -inf when a threat is detected
    }
    
    score = 0
    score += evaluation.road_strength(board, player) * weights['road_strength'] / max_values['road_strength']
    score += evaluation.flats_differential(board, player, opponent) * weights['flats_differential'] / max_values['flats_differential']
    score += evaluation.controlled_pieces(board, player) * weights['controlled_pieces'] / max_values['controlled_pieces']
    score += evaluation.blocking_potential(board, player) * weights['blocking_potential'] / max_values['blocking_potential']
    score += evaluation.stack_strength(board, player) * weights['stack_strength'] / max_values['stack_strength']
    score += evaluation.board_control(board, player) * weights['board_control'] / max_values['board_control']

    return score

def sort_moves(moves, board, player, opponent):
    """
    Sort moves based on a heuristic evaluation to improve alpha-beta pruning.
    """
    move_scores = []

    for move in moves:
        #new_state = copy.deepcopy(board)
        new_state = pickle.loads(pickle.dumps(board, -1))
        new_state = GameLogic.apply_action(new_state, move, player)
        score = evaluate_sort(new_state, player, opponent)
        move_scores.append((score, move))

    # Sort moves in descending order of score
    move_scores.sort(reverse=True, key=lambda x: x[0])

    # Return the sorted moves
    sorted_moves = [move for score, move in move_scores]
    return sorted_moves

def alpha_beta_pruning(board, player, opponent, player_reserves, opponent_reserves, alpha, beta, depth, maximizing_player, transposition_table, current_time, time_limit):
    start_time = time.time()
    board_key = pickle.dumps(board, -1)
    # Check if the position is in the transposition table
    if board_key in transposition_table:
        stored_depth, stored_value = transposition_table[board_key]
        if stored_depth >= depth:
            return stored_value

    if depth == 0:
        eval_score = evaluate(board, player, opponent)
        transposition_table[board_key] = (depth, eval_score)
        return eval_score
    else:
        win = GameLogic.check_win_conditions(board, player, player_reserves)
        if win[0]:
            eval_score = evaluate(board, player, opponent)
            transposition_table[board_key] = (depth, eval_score)
            return eval_score
    
    if maximizing_player:
        max_eval = float('-inf')
        moves = MoveGenerator.generate_moves(board, player, player_reserves)

        # SORT MOVES    
        moves = sort_moves(moves, board, player, opponent)
        for move in moves:
            new_state = pickle.loads(pickle.dumps(board, -1))
            #new_state = copy.deepcopy(board)
            new_player_reserves = player_reserves
            new_opponent_reserves = opponent_reserves

            new_state = GameLogic.apply_action(new_state, move, player)
            eval = alpha_beta_pruning(new_state, player, opponent, new_player_reserves, new_opponent_reserves, alpha, beta, depth - 1, False, transposition_table, time.time()-start_time, time_limit)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
            if time.time() - start_time + current_time > time_limit:
                break
        #transposition_table[board_key] = (depth, max_eval)
        return max_eval
    else:
        min_eval = float('inf')
        moves = MoveGenerator.generate_moves(board, opponent, opponent_reserves)

        # SORT MOVES
        moves = sort_moves(moves, board, opponent, player)
        for move in moves:
            #new_state = copy.deepcopy(board)
            new_state = pickle.loads(pickle.dumps(board, -1))
            new_player_reserves = player_reserves
            new_opponent_reserves = opponent_reserves

            new_state = GameLogic.apply_action(new_state, move, opponent)
            eval = alpha_beta_pruning(new_state, player, opponent, new_player_reserves, new_opponent_reserves, alpha, beta,  depth - 1, True, transposition_table, time.time()-start_time, time_limit)
            
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
            if time.time() - start_time + current_time > time_limit:
                break
        #transposition_table[board_key] = (depth, eval)
        return min_eval

def iterative_deepening(board, player, opponent, player_reserves, opponent_reserves, max_depth, maximizing_player, transposition_table, time_limit):
    """
    Method to limit search algorithm time wise.
    """
    start_time = time.time()
    best_move = None
    for depth in range(1, max_depth + 1):
        print(depth)
        best_eval = float('-inf')
        moves = MoveGenerator.generate_moves(board, player, player_reserves)
        moves = sort_moves(moves, board, player, opponent)
        for move in moves:
            new_state = pickle.loads(pickle.dumps(board, -1))
            new_player_reserves = player_reserves
            new_opponent_reserves = opponent_reserves
            new_state = GameLogic.apply_action(new_state, move, player)
            pickled_board = pickle.dumps(new_state, -1)
            # Check if the position is in the transposition table
            if pickled_board in transposition_table:
                stored_depth, stored_value = transposition_table[pickled_board]
                if stored_depth >= depth:
                    eval =  stored_value
                else:
                    eval = alpha_beta_pruning(new_state, player, opponent, new_player_reserves, new_opponent_reserves, float('-inf'), float('inf'), depth, not maximizing_player, transposition_table, time.time()-start_time, time_limit)

            else:
                eval = alpha_beta_pruning(new_state, player, opponent, new_player_reserves, new_opponent_reserves, float('-inf'), float('inf'), depth, not maximizing_player, transposition_table, time.time()-start_time, time_limit)
            if eval > best_eval:
                best_eval = eval
                best_move = move
            if time.time() - start_time > time_limit:
                print(f"Score = {best_eval} for {best_move}")
                return best_move
    print(f"Score = {best_eval} for {best_move}")
    return best_move

""" def iterative_deepening_worst(board, player, opponent, player_reserves, opponent_reserves, max_depth, maximizing_player, transposition_table, time_limit):
    #Method to limit search algorithm time wise.

    start_time = time.time()
    worst_move = None
    for depth in range(1, max_depth + 1):
        print(depth)
        worst_eval = float('inf')
        moves = MoveGenerator.generate_moves(board, player, player_reserves)
        for move in moves:
            new_state = pickle.loads(pickle.dumps(board, -1))
            new_player_reserves = player_reserves
            new_opponent_reserves = opponent_reserves

            new_state = GameLogic.apply_action(new_state, move, player)
            eval = alpha_beta_pruning(new_state, player, opponent, new_player_reserves, new_opponent_reserves, float('-inf'), float('inf'), depth, not maximizing_player, transposition_table)
            if eval < worst_eval:
                worst_eval = eval
                worst_move = move
            if time.time() - start_time > time_limit:
                print(f"Score = {worst_eval} for {worst_move}")
                return worst_move
    print(f"Score = {worst_eval} for {worst_move}")
    return worst_move """

def AI_first_move(board, player, player_reserves, opponent, opponent_reserves):
    moves = MoveGenerator.generate_placement_moves(board, player, player_reserves)
    worst_move = None
    worst_eval = float('inf')
    for move in moves:
        if move[0] == 'lay':
            new_state = pickle.loads(pickle.dumps(board, -1))
            new_player_reserves = player_reserves
            new_opponent_reserves = opponent_reserves
            new_state = GameLogic.apply_action(new_state, move, player)
            eval = evaluate(new_state, player, opponent)
            if eval < worst_eval:
                worst_eval = eval
                worst_move = move
    return worst_move
