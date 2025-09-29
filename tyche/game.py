from tyche.card import Deck
from tyche.player import Player

class Game:
    """
    Represents a game of Texas Hold'em.
    """
    def __init__(self, players):
        """
        Initializes a Game.

        Args:
            players (list): A list of Player objects.
        """
        self.players = players
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0

    def play_hand(self):
        """
        Plays one hand of Texas Hold'em.
        This is a placeholder for the full game logic.
        """
        print("Starting a new hand...")

        # 1. Shuffle deck
        self.deck = Deck()

        # 2. Deal hole cards
        for player in self.players:
            player.hand = [self.deck.deal(), self.deck.deal()]
            # print(f"Dealt {player.hand} to {player.name}") # Optional: for debugging

        # --- Placeholder for betting rounds and community cards ---
        print("Pre-flop betting round...")

        # Deal flop
        self.deck.deal() # Burn
        self.community_cards.extend([self.deck.deal() for _ in range(3)])
        print(f"Flop: {self.community_cards}")
        print("Post-flop betting round...")

        # Deal turn
        self.deck.deal() # Burn
        self.community_cards.append(self.deck.deal())
        print(f"Turn: {self.community_cards}")
        print("Post-turn betting round...")

        # Deal river
        self.deck.deal() # Burn
        self.community_cards.append(self.deck.deal())
        print(f"River: {self.community_cards}")
        print("Post-river betting round...")

        print("Showdown...")
        # In a full implementation, we would evaluate hands and award the pot.
        print("Hand complete.\n")


    def __repr__(self):
        return f"Game(players={[p.name for p in self.players]})"