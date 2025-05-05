# === File: minimax.py ===
from .eval_fun import evaluate_state
from .move_utils import get_valid_moves
from .board import AgentBoard
from referee.game import PlayerColor, Action, MoveAction, GrowAction

# def heuristic_sort(actions: Action, board, color: PlayerColor):

# def action_score(action):
#    if isinstance(action, MoveAction):
#        score = 0
#        score += len(action.directions) * 2
#        if color == PlayerColor.RED:
#            score += sum(dir.r for dir in action.directions)
#        else:
#            score -= sum(dir.r for dir in action.directions)
#        return score
#    elif isinstance(action, GrowAction):
#        return -1
#    else:
#        return 0

# return sorted(actions, key=action_score, reverse=True)


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
    # actions = heuristic_sort(actions, board, turn_color)

    best_action = None

    if maxPlayer:
        maxEval = float("-inf")
        for action in actions:
            new_board = board.copy()
            new_board.apply_action(action, turn_color)
            eval, _ = minimax(
                new_board, turn_color.opponent, depth - 1, alpha, beta, False, root_color,
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
