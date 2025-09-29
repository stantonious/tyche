from collections import Counter
from itertools import combinations

class Hand:
    """
    Represents a poker hand and provides methods for evaluation.
    A hand is ranked on a scale where higher is better.
    9: Royal Flush
    8: Straight Flush
    7: Four of a Kind
    6: Full House
    5: Flush
    4: Straight
    3: Three of a Kind
    2: Two Pair
    1: One Pair
    0: High Card
    """
    HAND_RANKS = {
        (9,): "Royal Flush", (8,): "Straight Flush", (7,): "Four of a Kind",
        (6,): "Full House", (5,): "Flush", (4,): "Straight",
        (3,): "Three of a Kind", (2,): "Two Pair", (1,): "One Pair", (0,): "High Card"
    }

    def __init__(self, hole_cards, community_cards):
        """
        Initializes a Hand.

        Args:
            hole_cards (list): A list of 2 Card objects.
            community_cards (list): A list of 3 to 5 Card objects.
        """
        self.all_cards = sorted(hole_cards + community_cards, reverse=True)
        self.best_hand_cards = []
        self.rank, self.best_hand_cards = self.evaluate_best_hand()

    def evaluate_best_hand(self):
        """
        Evaluates all 5-card combinations from the available 7 cards
        and returns the rank and cards of the best hand.
        """
        if len(self.all_cards) < 5:
            return (0, []), [] # Not enough cards for a full hand yet

        possible_hands = combinations(self.all_cards, 5)
        best_rank = (-1,)
        best_cards = []

        for hand_tuple in possible_hands:
            hand = list(hand_tuple)
            current_rank = self._evaluate_five_card_hand(hand)
            if self._compare_ranks(current_rank, best_rank) > 0:
                best_rank = current_rank
                best_cards = hand

        return best_rank, best_cards

    def _evaluate_five_card_hand(self, hand):
        """
        Evaluates a single 5-card hand and returns its rank as a tuple.
        The tuple structure allows for tie-breaking.
        e.g., (1, 12, 11, 5) -> One Pair, Queens, with J, 5 kickers.
        """
        hand = sorted(hand, reverse=True)
        values = [c.value for c in hand]
        suits = [c.suit for c in hand]

        is_flush = len(set(suits)) == 1
        is_straight = self._is_straight(values)

        # Royal/Straight Flush
        if is_straight and is_flush:
            if values[0] == 14: # Ace-high straight flush
                return (9,) + tuple(values) # Royal Flush
            return (8,) + tuple(values) # Straight Flush

        # Four of a Kind
        counts = Counter(values)
        if 4 in counts.values():
            four_value = [v for v, c in counts.items() if c == 4][0]
            kicker = [v for v, c in counts.items() if c == 1][0]
            return (7, four_value, kicker)

        # Full House
        if 3 in counts.values() and 2 in counts.values():
            three_value = [v for v, c in counts.items() if c == 3][0]
            pair_value = [v for v, c in counts.items() if c == 2][0]
            return (6, three_value, pair_value)

        # Flush
        if is_flush:
            return (5,) + tuple(values)

        # Straight
        if is_straight:
            return (4,) + tuple(values)

        # Three of a Kind
        if 3 in counts.values():
            three_value = [v for v, c in counts.items() if c == 3][0]
            kickers = sorted([v for v, c in counts.items() if c == 1], reverse=True)
            return (3, three_value) + tuple(kickers)

        # Two Pair
        if list(counts.values()).count(2) == 2:
            pairs = sorted([v for v, c in counts.items() if c == 2], reverse=True)
            kicker = [v for v, c in counts.items() if c == 1][0]
            return (2,) + tuple(pairs) + (kicker,)

        # One Pair
        if 2 in counts.values():
            pair_value = [v for v, c in counts.items() if c == 2][0]
            kickers = sorted([v for v, c in counts.items() if c == 1], reverse=True)
            return (1, pair_value) + tuple(kickers)

        # High Card
        return (0,) + tuple(values)

    def _is_straight(self, values):
        """Checks for a straight, handling the A-2-3-4-5 case."""
        # Ace-low straight (A, 5, 4, 3, 2) -> becomes (5, 4, 3, 2, 1)
        if values == [14, 5, 4, 3, 2]:
            return True
        # Standard straight
        return len(set(values)) == 5 and (values[0] - values[4] == 4)

    def _compare_ranks(self, rank1, rank2):
        """Compares two rank tuples. Returns > 0 if rank1 is better, < 0 if rank2 is better, 0 if equal."""
        for r1, r2 in zip(rank1, rank2):
            if r1 != r2:
                return r1 - r2
        return 0

    def get_rank_name(self):
        return self.HAND_RANKS.get((self.rank[0],), "Unknown")

    def __repr__(self):
        hand_str = ", ".join(map(str, self.best_hand_cards))
        return f"Hand({self.get_rank_name()} -> {hand_str})"

    def __gt__(self, other):
        return self._compare_ranks(self.rank, other.rank) > 0

    def __lt__(self, other):
        return self._compare_ranks(self.rank, other.rank) < 0

    def __eq__(self, other):
        return self._compare_ranks(self.rank, other.rank) == 0