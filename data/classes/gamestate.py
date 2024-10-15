from enum import Enum
class GameState(Enum):
    PLACE = 0
    MOVE = 1
    INFO = 2


class GameInit(Enum):
    RED = -1
    TITLE = 0
    BLUE = 1
    FINISHED = 2
    EXIT = 3
    CHOOSEOPPONENT = 4
    AI = 5
    HUMAN = 6
