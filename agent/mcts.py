import math
import random
import time
from .board import AgentBoard
from .move_utils import get_valid_moves
from referee.game import PlayerColor, Action, MoveAction, GrowAction, Coord, Direction

MAX_SIM_DEPTH = 30


class MCTS_node:
    def __init__(self, board: AgentBoard, turn_color: PlayerColor, parent):
        self.board = board
        self.turn_color = turn_color
        self.parent = parent
        self.wins = 0.0
        self.playouts = 0
        self.children = []
        self.actions = None

    def expand(self):

        if self.actions is None:
            self.actions = get_valid_moves(self.board, self.turn_color)
            random.shuffle(self.actions)

        action = self.actions.pop()

        next_board = self.board.copy()
        next_board.apply_action(action, self.turn_color)

        child = MCTS_node(next_board, self.turn_color.opponent, self)

        # Store the action together with child in a tuple
        self.children.append((child, action))

        return child

    def select(self, balance_weight=1.0):
        """
        Select a child based on UCB
        """
        max_ucb = 0.0
        max_child = None

        log_parent = math.log(self.playouts) if self.playouts != 0 else 0

        for child in self.children:
            if child[0].playouts == 0:
                return child

            exploit = -1.0 * (
                child[0].wins / child[0].playouts
            )  # times -1 for the parent opponent perspective
            explore = balance_weight * math.sqrt(log_parent / child[0].playouts)
            ucb = exploit + explore

            if ucb > max_ucb:
                max_ucb = ucb
                max_child = child[0]

        return max_child

    def update_backwards(self, result: float):
        """
        Update results backwards to parents in MCT
        """
        curr_node = self
        curr_res = result

        while curr_node:
            curr_node.playouts += 1
            curr_node.wins += curr_res

            curr_res *= -1.0
            curr_node = curr_node.parent


def search_best_action(
    root: MCTS_node, color: PlayerColor, time_limit: float, explore_weight: float
):
    curr_node = root
    start_time = time.perf_counter()

    while (time.perf_counter() - start_time) < time_limit:
        while curr_node is not None and not curr_node.board.is_game_over:
            if curr_node.actions is None or len(curr_node.actions) > 0:
                break
            curr_node = curr_node.select(explore_weight)

        if not curr_node.board.is_game_over and curr_node is not None:  # type: ignore
            if curr_node.actions is None or len(curr_node.actions) > 0:
                curr_node = curr_node.expand()

        # May need to tune the max_sim_depth with different values
        result_score = simulation(curr_node.board.copy(), curr_node.turn_color, 30)  # type: ignore
        curr_node.update_backwards(result_score)  # type: ignore

    return max(root.children, key=lambda child: child[0].playouts)[0]


def simulation(board: AgentBoard, player_color: PlayerColor, max_sim_depth: int):
    curr_state = board
    turn_color = player_color

    for i in range(max_sim_depth):
        if curr_state.is_game_over:
            return curr_state.get_game_result(player_color)

        actions = get_valid_moves(curr_state, turn_color)

        # TODO: may choose based on herustic
        action = random.choice(actions)
        curr_state.apply_action(action, turn_color)

        turn_color = turn_color.opponent

    # TODO: return evalution function result
    return
