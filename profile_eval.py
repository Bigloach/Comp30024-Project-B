import cProfile
import pstats
import io
import time
import numpy as np

from minimax.board import AgentBoard, PlayerColor, RED, BLUE, LILY, EMPTY, BOARD_N
from minimax.eval_fun import evaluate_state
from minimax.minimax import minimax_k, negamax

# from minimax_copy.eval_fun import evaluate_state
from referee.game import Coord


def create_complex_board_example():
    state = np.array(
        [
            [3, 0, 3, 0, 0, 3, 0, 3],
            [0, 3, 0, 2, 0, 0, 3, 0],
            [3, 1, 3, 0, 3, 1, 0, 3],
            [0, 2, 1, 2, 0, 3, 2, 0],
            [3, 0, 3, 1, 3, 1, 0, 3],
            [0, 2, 1, 0, 3, 2, 3, 0],
            [0, 0, 3, 0, 1, 0, 3, 0],
            [3, 3, 0, 0, 0, 0, 3, 3],
        ],
        dtype=np.int8,
    )
    red_frogs = {
        (2, 1),
        (2, 5),
        (3, 2),
        (4, 3),
        (4, 5),
        (6, 4),
    }
    blue_frogs = {
        (1, 3),
        (3, 1),
        (3, 3),
        (3, 6),
        (5, 1),
        (5, 5),
    }

    return AgentBoard(state, blue_frogs, red_frogs, turns=30)


def run_evaluation(board, color, iterations=1000):
    for i in range(iterations):
        evaluate_state(board, color)


def run_copy(board, iterations=1000):
    for i in range(iterations):
        board = board.copy()


def run_minimax(board, iterations=10):
    for i in range(iterations):
        killer_actions = [[None, None] for i in range(5)]
        for depth in range(1, 6):
            negamax(
                board.copy(),
                depth,
                PlayerColor.RED,
                float("-inf"),
                float("inf"),
                PlayerColor.RED,
                killer_actions,
            )


if __name__ == "__main__":
    board = create_complex_board_example()
    player = PlayerColor.RED

    profiler = cProfile.Profile()
    profiler.enable()

    run_minimax(board)
    profiler.disable()

    print("\n--- Profiling Report for Complex Board ---")
    s = io.StringIO()
    sort = pstats.SortKey.TIME
    ps = pstats.Stats(profiler, stream=s).sort_stats(sort)

    # print the first 30 rows
    ps.print_stats(20)
    print(s.getvalue())
    print("--- End Report ---")
