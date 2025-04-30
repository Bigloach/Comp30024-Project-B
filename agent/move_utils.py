from collections import deque
from .board import AgentBoard, BLUE, RED, LILY, EMPTY
from referee.game import (
    BOARD_N,
    PlayerColor,
    MoveAction,
    GrowAction,
    Coord,
    Direction,
)


def get_valid_moves(board: AgentBoard, color: PlayerColor):
    if color == PlayerColor.RED:
        directions = [
            Direction.Right,
            Direction.Left,
            Direction.Down,
            Direction.DownLeft,
            Direction.DownRight,
        ]
        player_frogs = board.reds
    else:
        directions = [
            Direction.Right,
            Direction.Left,
            Direction.Up,
            Direction.UpLeft,
            Direction.UpRight,
        ]
        player_frogs = board.blues

    valid_moves = []

    # The helper function for hops using BFS
    def get_valid_hops(src_cord: Coord):
        queue = deque([(src_cord, [])])
        # Visited keeps track of destinations reached via hops from src_cord
        visited = {src_cord}

        while queue:
            curr_pos, curr_path = queue.popleft()

            for dir in directions:
                try:
                    intermediate = curr_pos + dir
                    dest = intermediate + dir

                    # Check if destination is valid and not visited
                    if is_in_board(dest) and dest not in visited:
                        # Check if intermediate position has any frog to jump over
                        if (
                            board.state[intermediate.r, intermediate.c] == RED
                            or board.state[intermediate.r, intermediate.c] == BLUE
                        ):
                            if board.state[dest.r, dest.c] == LILY:
                                visited.add(dest)
                                valid_moves.append(MoveAction(src_cord, curr_path + [dir]))  # type: ignore
                                queue.append((dest, curr_path + [dir]))
                except ValueError:  # Catches coordinates out of board bound
                    continue

    # Iterate through each frog to find its possible moves (single steps and hops)
    for frog in player_frogs:
        for dir in directions:
            try:
                dest = frog + dir
                if is_in_board(dest) and board.state[dest.r, dest.c] == LILY:
                    valid_moves.append(
                        MoveAction(frog, dir)
                    )  # Single step is a path of length 1
            except ValueError:
                continue

        # Find all possible hop sequences starting from this frog
        get_valid_hops(frog)
        valid_moves.append(GrowAction())

    return valid_moves


def is_in_board(coord: Coord):
    return 0 <= coord.r < BOARD_N and 0 <= coord.c < BOARD_N
