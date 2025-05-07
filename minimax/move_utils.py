from collections import deque
from .board import AgentBoard, BLUE, RED, LILY, EMPTY, RED_DIRECTIONS, BLUE_DIRECTIONS
from .utils import is_within_board
from referee.game import (
    BOARD_N,
    PlayerColor,
    MoveAction,
    GrowAction,
    Coord,
    Direction,
)


RED_DIR = {
    Direction.DownRight: (1, 1),
    Direction.Down: (1, 0),
    Direction.DownLeft: (1, -1),
    Direction.Left: (0, -1),
    Direction.Right: (0, 1),
}

BLUE_DIR = {
    Direction.Up: (-1, 0),
    Direction.UpRight: (-1, 1),
    Direction.Right: (0, 1),
    Direction.Left: (0, -1),
    Direction.UpLeft: (-1, -1),
}


def get_valid_moves(board: AgentBoard, color: PlayerColor):
    if color == PlayerColor.RED:
        directions = RED_DIR
        player_frogs = board.reds
        target_row = BOARD_N - 1
    else:
        directions = BLUE_DIR
        player_frogs = board.blues
        target_row = 0

    valid_moves = []

    # The helper function for hops using BFS
    def get_valid_hops(src_cord: tuple):
        src = Coord(src_cord[0], src_cord[1])
        queue = deque([(src_cord, [])])

        # Visited keeps track of destinations reached via hops from src_cord
        visited = {src_cord}

        while queue:
            curr_pos, curr_path = queue.popleft()
            for dir, coord in directions.items():
                if curr_pos[0] == target_row:
                    continue
                try:
                    intermediate = (curr_pos[0] + coord[0], curr_pos[1] + coord[1])
                    dest = (intermediate[0] + coord[0], intermediate[1] + coord[1])

                    # Check if destination is valid and not visited
                    if (
                        is_within_board(intermediate)
                        and is_within_board(dest)
                        and dest not in visited
                    ):
                        # Check if intermediate position has any frog to jump over
                        if (
                            board.state[intermediate[0], intermediate[1]] == RED
                            or board.state[intermediate[0], intermediate[1]] == BLUE
                        ):
                            if board.state[dest[0], dest[1]] == LILY:
                                visited.add(dest)
                                new_path = curr_path + [dir]
                                valid_moves.append(MoveAction(src, new_path))
                                queue.append((dest, new_path))
                except (
                    ValueError,
                    IndexError,
                ):
                    continue

    # Iterate through each frog to find its possible moves (single steps and hops)
    for frog_t in player_frogs:
        for dir, coord in directions.items():
            if frog_t[0] == target_row:
                continue
            try:
                dest = (frog_t[0] + coord[0], frog_t[1] + coord[1])
                if is_within_board(dest) and board.state[dest[0], dest[1]] == LILY:
                    valid_moves.append(
                        MoveAction(Coord(frog_t[0], frog_t[1]), dir)
                    )  # Single step is a path of length 1
            except (ValueError, IndexError):
                continue
        # Find all possible hop sequences starting from this frog
        get_valid_hops(frog_t)

    valid_moves.append(GrowAction())

    return valid_moves
