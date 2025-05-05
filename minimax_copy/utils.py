from referee.game.constants import BOARD_N
from referee.game.coord import Coord


def is_in_board(coord: Coord):
    return 0 <= coord[0] < BOARD_N and 0 <= coord[1] < BOARD_N

def is_within_board(coord: tuple):
    return 0 <= coord[0] < BOARD_N and 0 <= coord[1] < BOARD_N
