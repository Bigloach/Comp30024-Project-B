# === File: minimax.py ===
from socket import herror
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
    if depth_lim == 0 or board.is_game_over():
        eval_score = evaluate_state(board, turn_color)
        return eval_score, None

    actions = get_valid_moves(board, turn_color)

    actions.sort(
        key=lambda x: action_heuristic(x, turn_color, killer_actions[depth_lim - 1]),
        reverse=True,
    )
    max_eval = float("-inf")
    max_action = None
    for action in actions:
        next_board = board.copy()
        next_board.apply_action(action, turn_color)
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
            killer_action = killer_actions[depth_lim - 1][0]
            if killer_action != action:
                killer_actions[depth_lim - 1][1] = killer_action
                killer_actions[depth_lim - 1][0] = action
            break

    return max_eval, max_action
