"""
This file contains evaluation function for cut off and
possible herustics for simulation
"""

from referee.game import PlayerColor
from referee.game.coord import Direction
from .board import BLUE_DIRECTIONS, LILY, RED, BLUE, EMPTY, RED_DIRECTIONS, AgentBoard
from .move_utils import is_in_board


def evaluate_state(board: AgentBoard, color: PlayerColor) -> float:
    own_color = RED if color == PlayerColor.RED else BLUE
    opp_color = BLUE if color == PlayerColor.RED else RED

    own_directions = RED_DIRECTIONS if color == PlayerColor.RED else BLUE_DIRECTIONS
    opp_directions = RED_DIRECTIONS if color == PlayerColor.BLUE else BLUE_DIRECTIONS

    own_frogs = board.reds if color == PlayerColor.RED else board.blues
    opp_frogs = board.blues if color == PlayerColor.RED else board.reds

    own_score = board.get_player_score(own_color)
    opp_score = board.get_player_score(opp_color)

    own_distances = sum(
        frog.r if color == PlayerColor.BLUE else (7 - frog.r) for frog in own_frogs
    )

    opp_distances = sum(
        frog.r if color == PlayerColor.RED else (7 - frog.r) for frog in opp_frogs
    )

    advancement = opp_distances - own_distances

    pad_count = 0
    for frog in own_frogs:
        for dir in own_directions:
            try:
                adj = frog + dir
                if is_in_board(adj) and board.state[adj.r, adj.c] == LILY:
                    pad_count += 1
            except ValueError:
                continue

    jump_opportunities = 0
    for frog in own_frogs:
        for dir in own_directions:
            try:
                mid = frog + dir
                dest = mid + dir
                if is_in_board(dest):
                    if (
                        board.state[mid.r, mid.c] in [RED, BLUE]
                        and board.state[dest.r, dest.c] == LILY
                    ):
                        jump_opportunities += 1
            except:
                continue

    threat_level = 0
    for frog in opp_frogs:
        for dir in opp_directions:
            try:
                mid = frog + dir
                dest = mid + dir
                if is_in_board(dest):
                    if (
                        board.state[mid.r, mid.c] in [RED, BLUE]
                        and board.state[dest.r, dest.c] == LILY
                    ):
                        threat_level += 1
            except:
                continue

    return float(
        100.0 * (own_score - opp_score)
        + 20.0 * advancement
        + 10.0 * pad_count 
        + 3.0 * jump_opportunities
        - 2.0 * threat_level
    )


def choose_with_herustic(actions):
    # TODO
    pass
