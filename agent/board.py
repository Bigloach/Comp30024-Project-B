import numpy as np

from referee.game.constants import BOARD_N, MAX_TURNS
from referee.game import PlayerColor, Coord, Direction, Action, MoveAction, GrowAction

# Defined states in the board
BLUE = 0
RED = 1
LILY = 2
EMPTY = 3

class AgentBoard:

    def __init__(self):
        self.state = np.zeros((BOARD_N, BOARD_N), dtype=int)

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

    def resolve_move(self, action: MoveAction, color: PlayerColor):

        if color == PlayerColor.RED:
            dest_state = RED
        else:
            dest_state = BLUE
        
        curr_pos = action.coord
        
        try:
            for dir in action.directions:
                curr_pos  = curr_pos + dir
        except ValueError:
            return 

        self.state[action.coord.r, action.coord.c] = EMPTY
        self.state[curr_pos.r, curr_pos.c] = dest_state
    
    def resolve_grow(self, color: PlayerColor):
        player_cells = set()  

        if color == PlayerColor.RED:
            turn_color = RED
        else:
            turn_color = BLUE

        for i in range(BOARD_N):
            for j in range(BOARD_N):
                if self.state[i,j] == turn_color:
                    player_cells.add(Coord(i,j))

        neighbour_cells = set()
        for cell in player_cells:
            for direction in Direction:
                try:
                    neighbour = cell + direction
                    neighbour_cells.add(neighbour)
                except ValueError:
                    pass
        for cell in neighbour_cells:
            if self.state[cell.r, cell.c] == EMPTY:
               self.state[cell.r, cell.c] = LILY 