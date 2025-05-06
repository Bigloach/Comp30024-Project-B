"""
This file contains evaluation function for cut off and
possible herustics for simulation
"""

from referee.game import PlayerColor
from referee.game.actions import Action, GrowAction, MoveAction
from referee.game.constants import BOARD_N
from referee.game.coord import Direction
from .board import (
    BLUE_DIRECTIONS,
    DIRECTION_DICT,
    LILY,
    RED,
    BLUE,
    EMPTY,
    RED_DIRECTIONS,
    AgentBoard,
)
from .utils import is_in_board


def evaluate_state(board: AgentBoard, color: PlayerColor) -> float:
    own_frogs = board.reds if color == PlayerColor.RED else board.blues
    opp_frogs = board.blues if color == PlayerColor.RED else board.reds
    own_directions = RED_DIRECTIONS if color == PlayerColor.RED else BLUE_DIRECTIONS
    opp_directions = BLUE_DIRECTIONS if color == PlayerColor.RED else RED_DIRECTIONS

    own_distances = 0
    row_sum = 0
    for frog in own_frogs:
        distance = frog[0] if color == PlayerColor.BLUE else (BOARD_N - 1 - frog[0])
        row_sum += frog[0]
        if (color == PlayerColor.RED and frog[0] >= 4) or (color == PlayerColor.BLUE and frog[0] <= 3):
            for dc in [-1, 0, 1]:
                col = frog[1] + dc
                if 0 <= col < BOARD_N:
                    row = frog[0] + 1 if color == PlayerColor.RED else frog[0] - 1
                    if 0 <= row < BOARD_N and board.state[row, col] in [RED, BLUE]:
                        distance += 1
        own_distances += distance

    opp_distances = 0
    for frog in opp_frogs:
        distance = frog[0] if color == PlayerColor.RED else (BOARD_N - 1 - frog[0])
        if (color == PlayerColor.RED and frog[0] <= 3) or (color == PlayerColor.BLUE and frog[0] >= 4):
            for dc in [-1, 0, 1]:
                col = frog[1] + dc
                if 0 <= col < BOARD_N:
                    row = frog[0] - 1 if color == PlayerColor.RED else frog[0] + 1
                    if 0 <= row < BOARD_N and board.state[row, col] in [RED, BLUE]:
                        distance += 1
        opp_distances += distance

    advancement = opp_distances - own_distances

    average_row = row_sum / len(own_frogs) if own_frogs else 0
    center_bias = -abs(average_row - (BOARD_N - 1 if color == PlayerColor.RED else 0))

    line_value = 0
    for frog in own_frogs:
        if (color == PlayerColor.RED and frog[0] >= BOARD_N - 2) or (color == PlayerColor.BLUE and frog[0] <= 1):
            end_row = BOARD_N - 1 if color == PlayerColor.RED else 0
            for col in range(BOARD_N):
                cell = board.state[end_row, col]
                if cell == LILY:
                    line_value += 4
                elif cell == EMPTY:
                    line_value += 3
                elif (cell == BLUE and color == PlayerColor.RED) or (cell == RED and color == PlayerColor.BLUE):
                    line_value += 2
                elif (cell == RED and color == PlayerColor.RED) or (cell == BLUE and color == PlayerColor.BLUE):
                    line_value += 1
            break

    return float(
        # 50.0 * (own_score - opp_score) +
        15.0 * advancement +
        1.0 * line_value
        # + 3.0 * center_bias
        # + 0.5 * pad_count
        # + 5.0 * jump_opportunities
        # + 4.0 * jump_used_bonus
        # - 4.0 * threat_level
    )


def action_heuristic(action: Action):
    heuristic = 0.0
    grow_score = 2.0
    forward_mult = 4
    if isinstance(action, GrowAction):
        return grow_score

    heuristic = heuristic + len(action.directions)
    for move in action.directions:
        dr, dc = DIRECTION_DICT[move]
        if dr != 0:
            heuristic += abs(dr * forward_mult)
        else:
            heuristic += 1
    return heuristic
