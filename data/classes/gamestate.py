from enum import Enum
class GameState(Enum):
    PLACE = 0
    MOVE = 1
    INFO = 2
    WRONG_STACK_MOVE = 3


class GameInit(Enum):
    RED = -1
    TITLE = 0
    BLUE = 1
