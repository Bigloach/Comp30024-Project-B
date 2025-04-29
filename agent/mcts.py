from .board import AgentBoard
from referee.game import PlayerColor, Action, MoveAction, GrowAction, Coord, Direction

def get_valid_moves(board: AgentBoard, color: PlayerColor):
    pass

class MCT_node: 
    def __init__(self, state, parent):
        