from enum import IntEnum

N = 6
M = 7
TARGET = 4


class PlayerEnum(IntEnum):
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2  # here was the issue it was a typo
    WINNER = 3
