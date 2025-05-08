"""
This file contains evaluation function for cut off and
possible herustics for simulation
"""

from minimax_copy.move_utils import BLUE_DIR, RED_DIR
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
from .utils import is_within_board


def evaluate_state(board: AgentBoard, color: PlayerColor) -> float:
    own_frogs = board.reds if color == PlayerColor.RED else board.blues
    opp_frogs = board.blues if color == PlayerColor.RED else board.reds
    own_directions = RED_DIR if color == PlayerColor.RED else BLUE_DIR
    own_distances = 0
    row_sum = 0
    col_counter = [0] * BOARD_N
    for frog in own_frogs:
        row_sum += frog[0]
        col_counter[frog[1]] += 1
        distance = frog[0] if color == PlayerColor.BLUE else (BOARD_N - 1 - frog[0])
        if (color == PlayerColor.RED and frog[0] >= 4) or (
            color == PlayerColor.BLUE and frog[0] <= 3
        ):
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
        if (color == PlayerColor.RED and frog[0] <= 3) or (
            color == PlayerColor.BLUE and frog[0] >= 4
        ):
            for dc in [-1, 0, 1]:
                col = frog[1] + dc
                if 0 <= col < BOARD_N:
                    row = frog[0] - 1 if color == PlayerColor.RED else frog[0] + 1
                    if 0 <= row < BOARD_N and board.state[row, col] in [RED, BLUE]:
                        distance += 1
        opp_distances += distance

    advancement = opp_distances - own_distances

    average_row = row_sum / (BOARD_N - 2)
    center_bias = -abs(average_row - (BOARD_N - 1 if color == PlayerColor.RED else 0))

    jump_opportunities = 0
    jump_used_bonus = 0
    for frog in own_frogs:
        for dir in own_directions.values():
            mid = (frog[0] + dir[0], frog[1] + dir[1])
            dest = (mid[0] + dir[0], mid[1] + dir[1])
            if is_within_board(dest):
                if (
                    board.state[mid[0], mid[1]] in [RED, BLUE]
                    and board.state[dest[0], dest[1]] == LILY
                ):
                    jump_opportunities += 1
                    if (color == PlayerColor.RED and dest[0] > frog[0]) or (
                        color == PlayerColor.BLUE and dest[0] < frog[0]
                    ):
                        jump_used_bonus += 1

    end_row = BOARD_N - 1 if color == PlayerColor.RED else 0
    line_value = 0
    dangerous_cols = set()
    for col in range(BOARD_N):
        cell = board.state[end_row, col]
        if cell == LILY:
            line_value += 4
        elif cell == EMPTY:
            line_value += 3
        elif (cell == BLUE and color == PlayerColor.RED) or (
            cell == RED and color == PlayerColor.BLUE
        ):
            line_value += 2
            dangerous_cols.add(col)
        elif (cell == RED and color == PlayerColor.RED) or (
            cell == BLUE and color == PlayerColor.BLUE
        ):
            line_value += 1
            dangerous_cols.add(col)

    spread_penalty = max(col_counter) - min(col_counter)
    column_avoidance_penalty = sum(col_counter[c] for c in dangerous_cols)

    return (
        15.0 * advancement
        + 1.0 * line_value
        + 3.0 * center_bias
        + 4.0 * jump_opportunities
        + 5.0 * jump_used_bonus
        - 2.0 * spread_penalty
        - 3.0 * column_avoidance_penalty
    )


def action_heuristic_color(action: Action, color: PlayerColor):
    heuristic = 0.0
    grow_score = 2.0
    forward_mult = 4.0
    forward_sign = 1
    forward_mult *= forward_sign
    if color == PlayerColor.BLUE:
        forward_sign = -1
    if isinstance(action, GrowAction):
        return grow_score

    heuristic = heuristic + len(action.directions)
    for move in action.directions:
        dr = DIRECTION_DICT[move][0]
        if dr != 0:
            heuristic += dr * forward_mult
        else:
            heuristic += 1
    return heuristic


def action_heuristic(action: Action):
    heuristic = 0.0
    grow_score = 2.0
    forward_mult = 4.0
    if isinstance(action, GrowAction):
        return grow_score

    heuristic = heuristic + len(action.directions)
    for move in action.directions:
        dr = DIRECTION_DICT[move][0]
        if dr != 0:
            heuristic += abs(dr * forward_mult)
        else:
            heuristic += 1
    return heuristic
