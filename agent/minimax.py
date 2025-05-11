# This file contains main minimax with alpha-beta pruning algorithm implementation
# through negamax

from .eval_fun import action_heuristic, evaluate_state
from .move_utils import get_valid_moves
from .board import AgentBoard
from referee.game import PlayerColor, Action, MoveAction, GrowAction


def negamax(
    board: AgentBoard,
    depth_lim: int,
    turn_color: PlayerColor,
    alpha: float,
    beta: float,
    killer_actions: list,
):
    """
    This function is the negamax with alpha-beta pruning implementation of minimax,
    the Max and min player alternation is implemented
    through negating the evaluation value of next turn
    """
    if depth_lim == 0 or board.is_game_over():
        eval_score = evaluate_state(board, turn_color)
        return eval_score, None

    actions = get_valid_moves(board, turn_color)

    # Order the moves based on heuristic
    actions.sort(
        key=lambda x: action_heuristic(x, turn_color, killer_actions[depth_lim - 1]),
        reverse=True,
    )
    max_eval = float("-inf")
    max_action = None
    for action in actions:
        next_board = board.copy()
        next_board.apply_action(action, turn_color)

        # Transform the original [alpha, beta] window to [-beta, -alpha]
        # for next turn, and negate the evaluation value
        eval_score = -negamax(
            next_board,
            depth_lim - 1,
            turn_color.opponent,
            -beta,
            -alpha,
            killer_actions,
        )[0]

        if eval_score > max_eval:
            max_eval = eval_score
            max_action = action

        if max_eval > alpha:
            alpha = max_eval

        if alpha >= beta:
            # Store the most recent killer action as first and shift
            # the original first to second killer action
            killer_action = killer_actions[depth_lim - 1][0]
            if killer_action != action:
                killer_actions[depth_lim - 1][1] = killer_action
                killer_actions[depth_lim - 1][0] = action
            break

    return max_eval, max_action
