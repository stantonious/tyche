import random
from tyche.hand import Hand
from tyche.action import Action, ActionType

class Player:
    """
    Represents a poker player.
    """
    def __init__(self, name, aggression, knowledge, inebriation, analytics, stack=1000):
        """
        Initializes a Player.

        Args:
            name (str): The name of the player.
            aggression (float): A value from 0 to 1 representing aggression.
            knowledge (float): A value from 0 to 1 representing game knowledge.
            inebriation (float): A value from 0 to 1 representing inebriation.
            analytics (float): A value from 0 to 1 representing analytical skill.
            stack (int): The player's starting chip stack.
        """
        self.name = name
        self.aggression = aggression
        self.knowledge = knowledge
        self.inebriation = inebriation
        self.analytics = analytics
        self.hand = []
        self.stack = stack
        self.is_active = True  # Is the player still in the hand?
        self.current_bet = 0  # Amount bet in the current round

    def make_decision(self, community_cards, current_bet_to_call, min_raise):
        """
        The player's decision-making engine. This is a simplified model.

        Args:
            community_cards (list): The community cards on the table.
            current_bet_to_call (int): The amount the player must call.
            min_raise (int): The minimum legal raise amount.

        Returns:
            Action: The action the player decides to take.
        """
        if not self.hand or not self.is_active:
            return Action(ActionType.FOLD)

        # 1. Evaluate hand strength
        full_hand = Hand(self.hand, community_cards)
        # Normalize hand rank (0=HighCard, 9=RoyalFlush) to a 0.0-1.0 scale
        hand_strength = full_hand.rank[0] / 9.0

        # 2. Factor in player attributes to get a decision score
        # Knowledge affects how accurately the player perceives their hand strength
        knowledge_mod = (1.0 - self.knowledge) * (random.random() - 0.5)  # +/- swing for low knowledge
        perceived_strength = max(0, min(1, hand_strength + knowledge_mod))

        # Aggression makes players more likely to bet/raise
        aggression_mod = (self.aggression - 0.5) * 0.3
        base_score = perceived_strength + aggression_mod

        # Inebriation adds random noise, making decisions less predictable
        inebriation_mod = (random.random() - 0.5) * self.inebriation
        final_score = max(0, min(1, base_score + inebriation_mod))

        # 3. Choose an action based on the score and game state
        can_check = current_bet_to_call == 0
        can_call = 0 < current_bet_to_call <= self.stack

        # Fold very weak hands if facing a bet
        if final_score < 0.2 and not can_check:
            return Action(ActionType.FOLD)

        # Bet or Raise with strong hands
        if final_score > 0.7:
            # Bet sizing is influenced by the 'analytics' attribute
            if self.analytics > 0.6:
                bet_amount = max(min_raise, int(self.stack * 0.25)) # More calculated bet
            else:
                bet_amount = max(min_raise, int(self.stack * random.uniform(0.1, 0.4))) # Less predictable

            if can_check: # No current bet, so we can bet
                if self.stack > bet_amount:
                    return Action(ActionType.BET, amount=bet_amount)
            else: # There is a bet, so we can raise
                raise_amount = bet_amount
                if self.stack > current_bet_to_call + raise_amount:
                    return Action(ActionType.RAISE, amount=raise_amount)

        # Default to checking or calling for medium hands or if unable to bet/raise
        if can_check:
            return Action(ActionType.CHECK)
        elif can_call:
            return Action(ActionType.CALL)
        else: # Cannot afford to call
            return Action(ActionType.FOLD)

    def reset_for_new_hand(self):
        """Resets player state for the start of a new hand."""
        self.hand = []
        self.is_active = True
        self.current_bet = 0

    def __repr__(self):
        return (f"Player(name={self.name}, stack={self.stack}, "
                f"hand={self.hand if self.hand else 'N/A'}, "
                f"is_active={self.is_active})")