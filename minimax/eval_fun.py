"""
This file contains evaluation function for cut off and
possible herustics for simulation
"""

from referee.game import PlayerColor
from referee.game.actions import MoveAction
from referee.game.constants import BOARD_N
from referee.game.coord import Direction
from .board import BLUE_DIRECTIONS, LILY, RED, BLUE, EMPTY, RED_DIRECTIONS, AgentBoard
from .utils import is_in_board


def evaluate_state(board: AgentBoard, color: PlayerColor) -> float:
    own_frogs = board.reds if color == PlayerColor.RED else board.blues
    opp_frogs = board.blues if color == PlayerColor.RED else board.reds
    own_directions = RED_DIRECTIONS if color == PlayerColor.RED else BLUE_DIRECTIONS
    opp_directions = BLUE_DIRECTIONS if color == PlayerColor.RED else RED_DIRECTIONS

    # own_score = board.get_player_score(RED if color == PlayerColor.RED else BLUE)
    # opp_score = board.get_player_score(BLUE if color == PlayerColor.RED else RED)

    own_distances = 0
    for frog in own_frogs:
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

    opp_distances = sum(
        frog[0] if color == PlayerColor.RED else (7 - frog[0]) for frog in opp_frogs
    )

    advancement = opp_distances - own_distances

    # pad_count = 0
    # for frog in own_frogs:
    #     for dir in own_directions:
    #         try:
    #             adj = frog + dir
    #             if is_in_board(adj) and board.state[adj.r, adj.c] == LILY:
    #                 pad_count += 1
    #         except ValueError:
    #             continue

    # jump_opportunities = 0
    # jump_used_bonus = 0
    # for frog in own_frogs:
    #     for dir in own_directions:
    #         try:
    #             mid = frog + dir
    #             dest = mid + dir
    #             if is_in_board(dest):
    #                 if (
    #                     board.state[mid.r, mid.c] in [RED, BLUE]
    #                     and board.state[dest.r, dest.c] == LILY
    #                 ):
    #                     jump_opportunities += 1
    #                     if (color == PlayerColor.RED and dest.r >= frog.r) or (color == PlayerColor.BLUE and dest.r <= frog.r):
    #                         jump_used_bonus += 1
    #         except:
    #             continue

    # threat_level = 0
    # for frog in opp_frogs:
    #     for dir in opp_directions:
    #         try:
    #             mid = frog + dir
    #             dest = mid + dir
    #             if is_in_board(dest):
    #                 if (
    #                     board.state[mid.r, mid.c] in [RED, BLUE]
    #                     and board.state[dest.r, dest.c] == LILY
    #                 ):
    #                     threat_level += 1
    #         except:
    #             continue

    line_value = 0
    for frog in own_frogs:
        if (color == PlayerColor.RED and frog[0] >= BOARD_N - 2) or (
            color == PlayerColor.BLUE and frog[0] <= 1
        ):
            end_row = BOARD_N - 1 if color == PlayerColor.RED else 0
            for col in range(BOARD_N):
                cell = board.state[end_row, col]
                if cell == LILY:
                    line_value += 10
                elif cell == EMPTY:
                    line_value += 5
                elif (cell == BLUE and color == PlayerColor.RED) or (
                    cell == RED and color == PlayerColor.BLUE
                ):
                    line_value += 2
                elif (cell == RED and color == PlayerColor.RED) or (
                    cell == BLUE and color == PlayerColor.BLUE
                ):
                    line_value += 1
            break

    return float(
        # 50 * (own_score - opp_score)
        +10 * advancement
        # + 3.0 * pad_count
        # + 5.0 * jump_opportunities
        # + 4.0 * jump_used_bonus
        # - 4.0 * threat_level
        + line_value
    )
