from enum import Enum
class GameState(Enum):

    
    PLACE = 2

    MOVE = 3

    INFO = 4


class GameInit(Enum):
    RED = -1
    TITLE = 0
    BLUE = 1
    FINISHED = 2
    EXIT = 3
