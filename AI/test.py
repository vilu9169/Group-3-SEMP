import AI.evaluation
import AI.board
import AI.GameAI
import pickle
import os
import AI.MoveGenerator
import AI.threat_assessment_2p
import optimized_threat
test_board = [[[0, 3], [0, 3], [0, 3], [0, 2]],
[[0], [0], [0], [0]],
[[0], [0], [0], [0, 2]],
[[0], [0], [0], [0, 2]]]
example = [[[0,3,3,3,3,2,2,2], [0], [0], [0]],
[[0], [0], [0], [0]],
[[0], [0], [0], [0]],
[[0], [0], [0], [0]]]

board.print_board(example)
board.move_stackAI(example, 0, 0, 1, 'down', [1, 2, 1], False)
board.print_board(example)
score = evaluation.road_strength(example, 2)
score = threat_assessment.threat_assessment(test_board)
print(score)

#moves = MoveGenerator.generate_stack_moves(example, 2)
#stacks = MoveGenerator.find_all_player_stacks(example, 2)
#print(moves)
#eval = GameAI.evaluate(example, 2, 1)
#print(eval)

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
test = str(example)
transposition_table = load_transposition_table()
print(len(transposition_table))