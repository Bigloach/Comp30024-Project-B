import numpy as np


from referee.game.constants import BOARD_N, MAX_TURNS
from referee.game import PlayerColor, Coord, Direction, Action, MoveAction, GrowAction

# Defined states in the board
EMPTY = 0
RED = 1
BLUE = 2
LILY = 3

RED_DIRECTIONS = [
    Direction.Right,
    Direction.Left,
    Direction.Down,
    Direction.DownLeft,
    Direction.DownRight,
]

BLUE_DIRECTIONS = [
    Direction.Right,
    Direction.Left,
    Direction.Up,
    Direction.UpLeft,
    Direction.UpRight,
]

DIRECTION_DICT = {
    Direction.Up: (-1, 0),
    Direction.UpRight: (-1, 1),
    Direction.Right: (0, 1),
    Direction.DownRight: (1, 1),
    Direction.Down: (1, 0),
    Direction.DownLeft: (1, -1),
    Direction.Left: (0, -1),
    Direction.UpLeft: (-1, -1),
}


class AgentBoard:

    def __init__(self, initial_state, initial_blue, initial_red, turns=0):
        self.state = initial_state
        self.reds = initial_red
        self.blues = initial_blue
        self.turns = turns

        if initial_state is None:
            self.state = np.zeros((BOARD_N, BOARD_N), dtype=np.int8)
            self.reds = set()
            self.blues = set()
            # Initialise the board states configuration
            for r in [0, BOARD_N - 1]:
                for c in [0, BOARD_N - 1]:
                    self.state[r, c] = LILY

            for r in [1, BOARD_N - 2]:
                for c in range(1, BOARD_N - 1):
                    self.state[r, c] = LILY

            for c in range(1, BOARD_N - 1):
                self.state[0, c] = RED
                self.state[BOARD_N - 1, c] = BLUE
                self.reds.add((0, c))
                self.blues.add((BOARD_N - 1, c))

    def apply_action(self, action: Action, color: PlayerColor):
        match action:
            case MoveAction(coord, direction):
                self.resolve_move(action, color)
            case GrowAction():
                self.resolve_grow(color)
            case _:
                raise IllegalActionException(f"Unknown action {action}", color)

    def resolve_move(self, action: MoveAction, color: PlayerColor):

        if color == PlayerColor.RED:
            dest_state = RED
        else:
            dest_state = BLUE

        action_r, action_c = action.coord.r, action.coord.c
        curr_pos_r, curr_pos_c = action_r, action_c
        is_single_move = self.is_single_move(action)

        if is_single_move:
            curr_pos_r += action.directions[0].r
            curr_pos_c += action.directions[0].c
        else:
            for dir in action.directions:
                curr_pos_r += dir.r + dir.r
                curr_pos_c += dir.c + dir.c

        self.state[action_r, action_c] = EMPTY
        self.state[curr_pos_r, curr_pos_c] = dest_state

        # Update red or blue set of the board
        if dest_state == RED:
            self.reds.remove((action_r, action_c))
            self.reds.add((curr_pos_r, curr_pos_c))
        else:
            self.blues.remove((action_r, action_c))
            self.blues.add((curr_pos_r, curr_pos_c))

        self.turns += 1

    def resolve_grow(self, color: PlayerColor):

        if color == PlayerColor.RED:
            player_cells = self.reds
        else:
            player_cells = self.blues

        neighbour_cells = set()
        for cell in player_cells:
            for direction in DIRECTION_DICT.values():
                neighbour = (cell[0] + direction[0], cell[1] + direction[1])
                if 0 <= neighbour[0] < BOARD_N and 0 <= neighbour[1] < BOARD_N:
                    neighbour_cells.add(neighbour)

        for cell in neighbour_cells:
            if self.state[cell[0], cell[1]] == EMPTY:
                self.state[cell[0], cell[1]] = LILY

        self.turns += 1

    def get_game_result(self, color: PlayerColor):
        winner = self.get_winner()

        if winner == color:
            return 1.0
        elif winner == color.opponent:
            return -1.0

        return 0.0

    def get_winner(self):
        if not self.is_game_over():
            return None
        red_score = self.get_player_score(RED)
        blue_score = self.get_player_score(BLUE)

        if red_score > blue_score:
            return PlayerColor.RED
        elif blue_score > red_score:
            return PlayerColor.BLUE

        return None

    def is_game_over(self):
        if self.turns >= MAX_TURNS:
            return True

        if (
            self.get_player_score(RED) == BOARD_N - 2
            or self.get_player_score(BLUE) == BOARD_N - 2
        ):
            return True

        return False

    def get_player_score(self, color: int):
        if color == RED:
            return np.sum(self.state[BOARD_N - 1, :] == RED)
        else:
            return np.sum(self.state[0, :] == BLUE)

    def is_single_move(self, action: MoveAction):
        if len(action.directions) == 1:
            dest = action.coord + action.directions[0]
            if self.state[dest.r, dest.c] == LILY:
                return True
        return False

    def copy(self):
        return AgentBoard(
            self.state.copy(), self.blues.copy(), self.reds.copy(), self.turns
        )
