from enum import Enum, auto

class ActionType(Enum):
    """
    Enum for the types of actions a player can take.
    """
    FOLD = auto()
    CHECK = auto()
    CALL = auto()
    BET = auto()
    RAISE = auto()

class Action:
    """
    Represents an action taken by a player.
    """
    def __init__(self, action_type, amount=0):
        """
        Initializes an Action.

        Args:
            action_type (ActionType): The type of action.
            amount (int, optional): The amount to bet or raise. Defaults to 0.
        """
        if not isinstance(action_type, ActionType):
            raise ValueError("action_type must be an instance of ActionType enum")

        self.action_type = action_type
        self.amount = amount

    def __repr__(self):
        if self.action_type in [ActionType.BET, ActionType.RAISE]:
            return f"Action({self.action_type.name}, amount={self.amount})"
        return f"Action({self.action_type.name})"