# === File: minimax.py ===
from socket import herror
from .eval_fun import action_heuristic, evaluate_state, action_heuristic_color
from .move_utils import get_valid_moves
from .board import AgentBoard
from referee.game import PlayerColor, Action, MoveAction, GrowAction


def minimax_k(
    board: AgentBoard,
    turn_color: PlayerColor,
    depth_lim: int,
    alpha: float,
    beta: float,
    maxPlayer: bool,
    root_color: PlayerColor,
    killer_actions: list,
):
    if depth_lim == 0 or board.is_game_over():
        return evaluate_state(board, root_color), None

    actions = get_valid_moves(board, turn_color)
    best_action = None

    heuristic_actions = []
    for killer_action in killer_actions[depth_lim - 1]:
        if killer_action and killer_action in actions:
            heuristic_actions.append(killer_action)
            actions.remove(killer_action)

    actions.sort(key=lambda x: action_heuristic_color(x, turn_color), reverse=True)
    heuristic_actions.extend(actions)

    if maxPlayer:
        maxEval = float("-inf")
        for action in heuristic_actions:
            new_board = board.copy()
            new_board.apply_action(action, turn_color)
            eval, _ = minimax_k(
                new_board,
                turn_color.opponent,
                depth_lim - 1,
                alpha,
                beta,
                False,
                root_color,
                killer_actions,
            )
            if eval > maxEval:
                maxEval = eval
                best_action = action
            alpha = max(alpha, eval)
            if beta <= alpha:
                killer_action = killer_actions[depth_lim - 1][0]
                if action != killer_action:
                    killer_actions[depth_lim - 1][1] = killer_action 
                    killer_actions[depth_lim - 1][0] = action
                break
        return maxEval, best_action
    else:
        minEval = float("inf")
        for action in heuristic_actions:
            new_board = board.copy()
            new_board.apply_action(action, turn_color)
            eval, _ = minimax_k(
                new_board,
                turn_color.opponent,
                depth_lim - 1,
                alpha,
                beta,
                True,
                root_color,
                killer_actions,
            )
            if eval < minEval:
                minEval = eval
                best_action = action
            beta = min(beta, eval)
            if beta <= alpha:
                killer_action = killer_actions[depth_lim - 1][0]
                if action != killer_action:
                    killer_actions[depth_lim - 1][1] = killer_action 
                    killer_actions[depth_lim - 1][0] = action
                break
        return minEval, best_action


def minimax(
    board: AgentBoard,
    turn_color: PlayerColor,
    depth_lim: int,
    alpha: float,
    beta: float,
    maxPlayer: bool,
    root_color: PlayerColor,
):
    if depth_lim == 0 or board.is_game_over():
        return evaluate_state(board, root_color), None

    actions = get_valid_moves(board, turn_color)
    best_action = None
    actions.sort(key=lambda x: action_heuristic_color(x, turn_color), reverse=True)

    if maxPlayer:
        maxEval = float("-inf")
        for action in actions:
            new_board = board.copy()
            new_board.apply_action(action, turn_color)
            eval, _ = minimax(
                new_board,
                turn_color.opponent,
                depth_lim - 1,
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
                new_board,
                turn_color.opponent,
                depth_lim - 1,
                alpha,
                beta,
                True,
                root_color,
            )
            if eval < minEval:
                minEval = eval
                best_action = action
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, best_action
