# === File: minimax.py ===
from .eval_fun import evaluate_state
from .move_utils import get_valid_moves
from .board import AgentBoard
from referee.game import PlayerColor, Action, MoveAction, GrowAction


def minimax(
    board: AgentBoard,
    turn_color: PlayerColor,
    depth: int,
    alpha: float,
    beta: float,
    maxPlayer: bool,
    root_color: PlayerColor,
):
    if depth == 0 or board.is_game_over():
        return evaluate_state(board, root_color), None

    actions = get_valid_moves(board, turn_color)
    if maxPlayer:
        maxEval = float("-inf")
        for action in actions:
            new_board = board.copy()
            new_board.apply_action(action, turn_color)
            eval, _ = minimax(
                new_board,
                turn_color.opponent,
                depth - 1,
                alpha,
                beta,
                False,
                root_color,
            )
            if eval > maxEval:
                maxEval = eval
                best_action = action
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, best_action
    else:
        minEval = float("inf")
        for action in actions:
            new_board = board.copy()
            new_board.apply_action(action, turn_color)
            eval, _ = minimax(
                new_board, turn_color.opponent, depth - 1, alpha, beta, True, root_color
            )
            if eval < minEval:
                minEval = eval
                best_action = action
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, best_action
