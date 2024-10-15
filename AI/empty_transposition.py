import os
import pickle
# Path to save the empty transposition table
TRANS_TABLE_PATH = "transposition_table.pkl"

# Create an empty dictionary as the initial transposition table
empty_table = {}

# Save the empty table to a .pkl file
with open(TRANS_TABLE_PATH, 'wb') as f:
    pickle.dump(empty_table, f)

print(f"Empty transposition table saved to {TRANS_TABLE_PATH}")