# Game Document

# Running the Game
1. Navigate to the game folder
2. In the terminal, enter: "python main.py"

## Game Flow

1. Player 1 chooses a color, either red or blue
    1.1. Both players start with 15 pieces.
2. Round 1: Each player gets to place one piece of the opponents color.

3. Subesquent rounds players take turns either placing or moving a piece of their own color
    3.1. Players can place either a 'Standing' or 'Laying' piece.
    3.2 'Standing' pieces can not have other pieces place on top of it
    3.3 'Laying' pieces may have other pieces placed on top of it, creating a stack that can be moved.

4. A player wins once they have created a line, vertical or horizontal, connecting one side to the opposite side with same coulored 'Laying' pieces.
    4.1. In the event that there are no legal moves and both players are out of pieces, the player with most 'Laying' pieces on top wins. If they have an equal amount of pieces on top the game ends a tie.

## Legal Moves
1. Any piece may move to one adjacent square, as long as it does not move outside of the board or if the move places the moved piece on a 'Standing' piece
2. Stacks may move several squares in one move according to the following rules:

    2.1 You may split the stack, but the bottom piece must be of your own color.
   
    2.2 When you move the stack you leave the bottom piece for each square you traverse.
   
    2.3 The amount of squares you can traverse is determined by the amount of pieces of your color is at the bottom of the stack.


