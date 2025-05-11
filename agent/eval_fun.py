# This file contains evaluation function for cut off and
# possible herustics for simulation

from .move_utils import BLUE_DIR, RED_DIR
from referee.game import PlayerColor
from referee.game.actions import Action, GrowAction
from referee.game.constants import BOARD_N
from .board import (
    DIRECTION_DICT,
    LILY,
    RED,
    BLUE,
    EMPTY,
    AgentBoard,
)


def evaluate_state(board: AgentBoard, color: PlayerColor) -> float:
    """
    This function evaluates a board state
    based on color
    """
    if color == PlayerColor.RED:
        player_frogs = board.reds
        opponent_frogs = board.blues
        player_directions = RED_DIR
    else:
        player_frogs = board.blues
        opponent_frogs = board.reds
        player_directions = BLUE_DIR

    if color == PlayerColor.RED:
        color = RED
    else:
        color = BLUE

    col_dirs = [-1, 0, 1]
    player_distances = 0
    row_sum = 0
    col_frogs = [0] * BOARD_N
    for frog in player_frogs:
        row_sum += frog[0]
        col_frogs[frog[1]] += 1
        if color == BLUE:
            distance = frog[0]
        else:
            distance = BOARD_N - 1 - frog[0]
        if (color == RED and frog[0] >= 4) or (color == BLUE and frog[0] <= 3):
            for dir in col_dirs:
                col = frog[1] + dir
                if 0 <= col < BOARD_N:
                    row = frog[0] + 1 if color == RED else frog[0] - 1
                    if 0 <= row < BOARD_N and board.state[row, col] in [RED, BLUE]:
                        distance += 1
        player_distances += distance

    opponent_distances = 0
    for frog in opponent_frogs:
        if color == RED:
            distance = frog[0]
        else:
            distance = BOARD_N - 1 - frog[0]
        if (color == RED and frog[0] <= 3) or (color == BLUE and frog[0] >= 4):
            for dir in col_dirs:
                col = frog[1] + dir
                if 0 <= col < BOARD_N:
                    row = frog[0] - 1 if color == RED else frog[0] + 1
                    if 0 <= row < BOARD_N and board.state[row, col] in [RED, BLUE]:
                        distance += 1
        opponent_distances += distance

    average_row = row_sum / (BOARD_N - 2)
    central_adjust = abs(average_row - (BOARD_N - 1 if color == RED else 0))

    hop_forward = 0
    hop_opporunities = 0
    for frog in player_frogs:
        for dir in player_directions.values():
            mid = (frog[0] + dir[0], frog[1] + dir[1])
            dest = (mid[0] + dir[0], mid[1] + dir[1])
            if 0 <= dest[0] < BOARD_N and 0 <= dest[1] < BOARD_N:
                if (
                    board.state[mid[0], mid[1]] in [RED, BLUE]
                    and board.state[dest[0], dest[1]] == LILY
                ):
                    hop_opporunities += 1
                    if (color == RED and dest[0] > frog[0]) or (
                        color == BLUE and dest[0] < frog[0]
                    ):
                        hop_forward += 1

    target_row = BOARD_N - 1 if color == RED else 0
    line_value = 0
    blocking_cols = set()
    for col in range(BOARD_N):
        cell = board.state[target_row, col]
        if cell == LILY:
            line_value += 4
        elif cell == EMPTY:
            line_value += 3
        elif cell != color:
            line_value += 2
            blocking_cols.add(col)
        elif cell == color:
            line_value += 1
            blocking_cols.add(col)

    uneven_frogs_penalty = max(col_frogs) - min(col_frogs)
    column_blocking = sum(col_frogs[c] for c in blocking_cols)

    return (
        15.0 * opponent_distances
        + line_value
        + 1 * hop_opporunities
        + 5 * hop_forward
        - 15 * player_distances
        - 3 * central_adjust
        - 2 * uneven_frogs_penalty
        - 3 * column_blocking
    )


def action_heuristic(action: Action, color: PlayerColor, killer_actions):
    """
    This function assigns heuristic priority to a action
    based on static evaluation and killer heuristic
    """
    heuristic = 0.0
    grow_score = 2.0
    forward_mult = 4.0
    forward_sign = 1
    killer_score = 100.0
    forward_mult *= forward_sign

    if killer_actions is not None:
        # Assign the first killer action with highest priority
        if action == killer_actions[0]:
            return killer_score
        elif action == killer_actions[1]:
            return killer_score - 1

    if color == PlayerColor.BLUE:
        forward_sign = -1

    if isinstance(action, GrowAction):
        return grow_score

    # Assign priority based on static evaluation
    heuristic = heuristic + len(action.directions)
    for move in action.directions:
        m_forward = DIRECTION_DICT[move][0]
        if m_forward != 0:
            heuristic += m_forward * forward_mult
        else:
            heuristic += 1
    return heuristic
