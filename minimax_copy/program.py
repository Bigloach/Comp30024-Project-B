# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part B: Game Playing Agent

from referee.game.actions import GrowAction
from .minimax import negamax
from .board import AgentBoard
from referee.game import PlayerColor, Action
import time

DEPTH = 5
MAX_TURNS = 75
MAX_TURN_TIME = 10.0


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
        self.turns = 1
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

        killer_actions = [[None, None] for i in range(DEPTH)]

        time_rem = referee["time_remaining"]
        curr_turn = self.turns
        start_time = time.process_time()
        if curr_turn == MAX_TURNS:
            allowed_time = time_rem
        else:
            if curr_turn <= 10:
                allowed_time = (time_rem / (MAX_TURNS - self.turns)) * 0.7
            elif curr_turn <= 40:
                allowed_time = (time_rem / (MAX_TURNS - self.turns)) * 1.6
            else:
                allowed_time = time_rem / (MAX_TURNS - self.turns)

        if allowed_time > MAX_TURN_TIME:
            allowed_time = MAX_TURN_TIME

        for depth in range(1, DEPTH + 1):
            best_action = negamax(
                self.board.copy(),
                depth,
                self._color,
                float("-inf"),
                float("inf"),
                killer_actions,
            )[1]
            if time.process_time() - start_time > allowed_time:
                break

        self.turns += 1
        return best_action

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
