from enum import Enum
class GameState(Enum):
    RED = -1
    TITLE = 0
    BLUE = 1
    
    PLACE = 2

    MOVE = 3

    INFO = 4


class GameInit(Enum):
    RED = -1
    TITLE = 0
    BLUE = 1
