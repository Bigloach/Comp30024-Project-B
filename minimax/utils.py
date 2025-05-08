from referee.game.constants import BOARD_N
from referee.game.coord import Coord


def is_in_board(coord: Coord):
    return 0 <= coord.r < BOARD_N and 0 <= coord.c < BOARD_N
