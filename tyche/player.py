class Player:
    """
    Represents a poker player.
    """
    def __init__(self, name, aggression, knowledge, inebriation, analytics):
        """
        Initializes a Player.

        Args:
            name (str): The name of the player.
            aggression (float): A value from 0 to 1 representing aggression.
            knowledge (float): A value from 0 to 1 representing game knowledge.
            inebriation (float): A value from 0 to 1 representing inebriation.
            analytics (float): A value from 0 to 1 representing analytical skill.
        """
        self.name = name
        self.aggression = aggression
        self.knowledge = knowledge
        self.inebriation = inebriation
        self.analytics = analytics
        self.hand = []
        self.stack = 0

    def __repr__(self):
        return (f"Player(name={self.name}, "
                f"aggression={self.aggression}, "
                f"knowledge={self.knowledge}, "
                f"inebriation={self.inebriation}, "
                f"analytics={self.analytics})")