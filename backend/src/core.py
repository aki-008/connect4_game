#  game core logic

from collections.abc import Callable
from dataclasses import dataclass

from .constants import TARGET, M, N, PlayerEnum


@dataclass
class Direction:
    name: str
    conditions: Callable[[int, int], bool]
    function: Callable[[list[list[int]], int, int, int], int]
    move_condition: Callable[[int, int, int], bool]
    move_row_col: Callable[[int, int, int], tuple[int, int]]


DIRECTIONS = [
    Direction(
        name="down",
        conditions=lambda row, _: row < 3,
        function=lambda board, row, cols, i: board[row + i][cols],
        move_condition=lambda row, cols, i: row + i < N,
        move_row_col=lambda row, cols, i: (row + i, cols),
    ),
    Direction(
        name="right",
        conditions=lambda _, cols: cols <= 3,
        function=lambda board, row, cols, i: board[row][cols + i],
        move_condition=lambda row, cols, i: cols + i < M,
        move_row_col=lambda row, cols, i: (row, cols + i),
    ),
    Direction(
        name="left down",
        conditions=lambda row, cols: row <= 2 and cols >= 3,
        function=lambda board, row, cols, i: board[row + i][cols - i],
        move_condition=lambda row, cols, i: row + i < N and cols - i >= 0,
        move_row_col=lambda row, cols, i: (row + i, cols - i),
    ),
    Direction(
        name="right down",
        conditions=lambda row, cols: row <= 2 and cols <= 3,
        function=lambda board, row, cols, i: board[row + i][cols + i],
        move_condition=lambda row, cols, i: row + i < N and cols + i < M,
        move_row_col=lambda row, cols, i: (row + i, cols + i),
    ),
]


def init_board() -> list[list[int]]:
    return [[PlayerEnum.EMPTY for _ in range(M)] for _ in range(N)]


def calculate_row_by_col(board: list[list[int]], col: int) -> int | None:
    if col < 0 or col >= M:
        return None
    for row in range(N - 1, -1, -1):
        if board[row][col] == PlayerEnum.EMPTY:
            return row
    return None


def is_valid_move(board: list[list[int]], row: int | None, cols: int | None) -> bool:
    if row is None or cols is None:
        return False
    if row < 0 or row >= N or cols < 0 or cols >= M:
        return False
    if board[row][cols] != PlayerEnum.EMPTY:
        return False
    return row == N - 1 or board[row + 1][cols] != PlayerEnum.EMPTY


def detect_winner(board: list[list[int]]) -> int | None:
    def check_direction(row: int, cols: int) -> bool:
        value = board[row][cols]

        for direction in DIRECTIONS:
            if direction.conditions(row, cols):
                for i in range(1, TARGET):
                    if direction.function(board, row, cols, i) != value:
                        break
                else:
                    return True
        return False

    for i in range(N):
        for j in range(M):
            if board[i][j] != PlayerEnum.EMPTY and check_direction(i, j):
                return board[i][j]
    return None


def mark_winner(board: list[list[int]], winner: int) -> None:
    def find_winner_cells(row: int, col: int) -> None:
        for direction in DIRECTIONS:
            line = []

            i = 0
            while (
                direction.move_condition(row, col, i)
                and direction.function(board, row, col, i) == winner
            ):
                line.append(direction.move_row_col(row, col, i))
                i += 1

            if len(line) >= TARGET:
                winner_cells.extend(line)

    winner_cells: list[tuple[int, int]] = []
    for i in range(N):
        for j in range(M):
            if board[i][j] == winner:
                find_winner_cells(i, j)

    for row, col in set(winner_cells):
        board[row][col] = PlayerEnum.WINNER
