# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part B: Game Playing Agent

from .mcts import MCTS_node, search_best_action
from .board import AgentBoard
from referee.game import PlayerColor, Coord, Direction, Action, MoveAction, GrowAction

TIME_FRACTION = 0.05
MAX_TURN_TIME = 3.5
MIN_TURN_TIME = 0.3

class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Freckers game events.
    """

    def __init__(self, color: PlayerColor, **referee: dict):
        """
        This constructor method runs when the referee instantiates the agent.
        Any setup and/or precomputation should be done here.
        """
        self._color = color
        self.board = AgentBoard(None, None, None)
        self.mcts_root = None

        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as RED")
            case PlayerColor.BLUE:
                print("Testing: I am playing as BLUE")

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object.
        """

        # Below we have hardcoded two actions to be played depending on whether
        # the agent is playing as BLUE or RED. Obviously this won't work beyond
        # the initial moves of the game, so you should use some game playing
        # technique(s) to determine the best action to take.

        time_remaining = referee["time_remaining"]
        time_limit = MAX_TURN_TIME
        BOUNDRY = 0.05

        if time_remaining > BOUNDRY:  # type: ignore
            calculated_limit = time_remaining * TIME_FRACTION  # type: ignore
            time_limit = min(MAX_TURN_TIME, time_remaining - BOUNDRY, calculated_limit)  # type: ignore
            time_limit = max(MIN_TURN_TIME, time_limit)
            if time_remaining < MIN_TURN_TIME + BOUNDRY:  # type: ignore
                time_limit = max(0.01, time_remaining - BOUNDRY)  # type: ignore

        else:
            time_limit = MIN_TURN_TIME

        time_limit = max(0.01, time_limit)
        if (
            self.mcts_root is None
            or self.mcts_root.board.state.tobytes() != self.board.state.tobytes()  # type: ignore
        ):
            self.mcts_root = MCTS_node(self.board.copy(), self._color, None)

        child, action = search_best_action(self.mcts_root, time_limit)  # type: ignore

        if child:
            self.mcts_root = child
            self.mcts_root.parent = None

        return action

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after a player has taken their
        turn. You should use it to update the agent's internal game state.
        """

        # There are two possible action types: MOVE and GROW. Below we check
        # which type of action was played and print out the details of the
        # action for demonstration purposes. You should replace this with your
        # own logic to update your agent's internal game state representation.
        self.board.apply_action(action, color)
        if color == self._color.opponent and self.mcts_root is not None:
            for child in self.mcts_root.children:
                if child[1] == action:
                    self.mcts_root = child[0]
                    self.mcts_root.parent = None
                    return

        self.mcts_root = None
