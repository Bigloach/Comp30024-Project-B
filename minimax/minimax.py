# === File: minimax.py ===
from socket import herror
from .eval_fun import action_heuristic, action_heuristic_1, evaluate_state
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

    actions.sort(
        key=lambda x: action_heuristic_1(x, turn_color),
        reverse=True,
    )
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


def negamax(
    board: AgentBoard,
    depth_lim: int,
    turn_color: PlayerColor,
    alpha: float,
    beta: float,
    player_color: PlayerColor,
    killer_actions: list,
):
    if depth_lim == 0 or board.is_game_over():
        eval_score = evaluate_state(board, player_color)
        if turn_color == player_color:
            return eval_score, None
        else:
            return -eval_score, None

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
            player_color,
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
