"""
This file contains evaluation function for cut off and
possible herustics for simulation
"""

import random
from referee.game import PlayerColor
from referee.game.actions import MoveAction
from referee.game.constants import BOARD_N
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
        for dir in own_directions[2:]:
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
            except ValueError:
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
            except ValueError:
                continue

    return float(
        #100.0 * (own_score - opp_score) +
        75.0 * advancement
        + 10.0 * pad_count 
        + 5.0 * jump_opportunities
        - 2.0 * threat_level
    )


def choose_with_heuristic(actions, board: AgentBoard, color: PlayerColor):
    END_SCORE = 15.0
    HOP_SCORE = 6.0
    FORWARD_SCORE = 5.0
    FORWARD_MULT = 2.0
    GROW_SCORE = 0.5

    if len(actions) == 1:
        return actions[0]
    dest_row = BOARD_N - 1 if color == PlayerColor.RED else 0

    action_scores = []
    for action in actions:
        score = 1.0 
        if isinstance(action, MoveAction):
            start = action.coord
            dest = action.coord
            if not board.is_single_move(action):
                for dir in action.directions:
                    dest = dest + dir + dir
                score += HOP_SCORE
            else:
                dest += action.directions[0]
            
            forward = abs(dest.r - start.r)
            if forward > 0:
                score += FORWARD_SCORE
            score += forward * FORWARD_MULT

            if dest.r == dest_row:
                score += END_SCORE 
         
        action_scores.append(score)

    return random.choices(actions, weights=action_scores, k=1)[0]
