from typing import Optional
from .board import AgentBoard
from .move_utils import get_valid_moves
from referee.game import PlayerColor, Action, MoveAction, GrowAction, Coord, Direction

    
class MCTS_node: 
    def __init__(self, board: AgentBoard, turn_color: PlayerColor, parent):
        self.board = board
        self.turn_color = turn_color 
        self.parent = parent
        self.wins = 0.0
        self.playouts = 0
        self.successors = []
        self.actions = None

    def get_game_result(self):

        winner = self.board.get_winner()
        
        if winner == self.turn_color:
            return 1.0
        elif winner == self.turn_color.opponent:
            return -1.0 
        
        return 0.0
    
    def expand_node(self):
        # TODO
        pass

    def UCB_select(self):
        # TODO
        pass
    
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
