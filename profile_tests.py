import cProfile
import pstats
import io
import numpy as np

from minimax.board import AgentBoard, PlayerColor, RED, BLUE, LILY, EMPTY, BOARD_N
from minimax.eval_fun import evaluate_state
from minimax.minimax import negamax


def generate_complex_board():
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


def test_evaluation(board, color, iterations=1000):
    for i in range(iterations):
        evaluate_state(board, color)


def test_copy(board, iterations=1000):
    for i in range(iterations):
        board = board.copy()


def test_minimax(board, iterations=10):
    for i in range(iterations):
        killer_actions = [[None, None] for i in range(5)]
        for depth in range(1, 6):
            negamax(
                board.copy(),
                5,
                PlayerColor.BLUE,
                float("-inf"),
                float("inf"),
                killer_actions,
            )


if __name__ == "__main__":
    board = generate_complex_board()
    player = PlayerColor.RED

    profiler = cProfile.Profile()
    profiler.enable()

    test_minimax(board)
    profiler.disable()

    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats(pstats.SortKey.TIME)

    # print the first 20 rows
    ps.print_stats(20)
    print(s.getvalue())
