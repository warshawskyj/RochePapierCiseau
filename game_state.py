from enum import Enum


class GameState(Enum):
    NOT_STARTED = 0
    GAME_OVER = 1
    ROUND_DONE = 2
    ROUND_ACTIVE = 3


class GameOutcome(Enum):
    PLAYER_WON = 0
    COMPUTER_WON = 1
    DRAW = 2
