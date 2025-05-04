# === File: minimax.py ===
from .eval_fun import evaluate_state
from .move_utils import get_valid_moves
from .board import AgentBoard
from referee.game import PlayerColor, Action, MoveAction, GrowAction


class MinimaxNode:
    def __init__(self, board, turn_color: PlayerColor, parent=None):
        self.board = board
        self.turn_color = turn_color
        self.parent = parent
        self.children = []
        self.actions = None

    def expand(self):
        if self.actions is None:
            self.actions = get_valid_moves(self.board, self.turn_color)

        if not self.actions:
            return None

        action = self.actions.pop()
        next_board = self.board.copy()
        next_board.apply_action(action, self.turn_color)

        child = MinimaxNode(next_board, self.turn_color.opponent, self)
        self.children.append((child, action))
        return child

    def fully_expanded(self):
        return self.actions is not None and len(self.actions) == 0


# def minimax(
#     node: MinimaxNode,
#     depth: int,
#     alpha: float,
#     beta: float,
#     maximizingPlayer: bool,
#     color: PlayerColor,
# ):
#     if depth == 0 or node.board.is_game_over():
#         return evaluate_state(node.board, color), None

#     current_color = color if maximizingPlayer else color.opponent

#     if node.actions is None:
#         node.actions = get_valid_moves(node.board, current_color)

#     best_action = None

#     if maximizingPlayer:
#         maxEval = float("-inf")
#         for action in node.actions:
#             new_board = node.board.copy()
#             new_board.apply_action(action, current_color)
#             child_node = MinimaxNode(new_board, current_color.opponent, node)
#             eval, _ = minimax(child_node, depth - 1, alpha, beta, False, color)
#             if eval > maxEval:
#                 maxEval = eval
#                 best_action = action
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         return maxEval, best_action

#     else:
#         minEval = float("inf")
#         for action in node.actions:
#             new_board = node.board.copy()
#             new_board.apply_action(action, current_color)
#             child_node = MinimaxNode(new_board, current_color.opponent, node)
#             eval, _ = minimax(child_node, depth - 1, alpha, beta, True, color)
#             if eval < minEval:
#                 minEval = eval
#                 best_action = action
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         return minEval, best_action


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
