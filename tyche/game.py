from tyche.card import Deck
from tyche.player import Player
from tyche.action import Action, ActionType
from tyche.hand import Hand

class Game:
    """
    Represents and manages a single game of Texas Hold'em.
    """
    def __init__(self, players, small_blind=5, big_blind=10):
        """
        Initializes a Game.

        Args:
            players (list): A list of Player objects.
            small_blind (int): The amount of the small blind.
            big_blind (int): The amount of the big_blind.
        """
        self.players = players
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.dealer_pos = 0

    def play_hand(self):
        """
        Plays one complete hand of Texas Hold'em.
        """
        print("="*10 + " Starting a New Hand " + "="*10)

        # 1. Reset players and deck for the new hand
        self._reset_for_new_hand()
        active_players = self._get_active_players()
        if len(active_players) < 2:
            print("Not enough players to continue.")
            return

        # 2. Post blinds
        self._post_blinds(active_players)
        print(f"Pot after blinds: {self.pot}")

        # 3. Deal hole cards
        self._deal_hole_cards(active_players)

        # 4. Pre-flop betting round
        self._run_betting_round()
        if len(self._get_active_players()) == 1:
            self._award_pot_to_winner()
            return

        # 5. Flop
        self._deal_community_cards("Flop", 3)
        self._run_betting_round()
        if len(self._get_active_players()) == 1:
            self._award_pot_to_winner()
            return

        # 6. Turn
        self._deal_community_cards("Turn", 1)
        self._run_betting_round()
        if len(self._get_active_players()) == 1:
            self._award_pot_to_winner()
            return

        # 7. River
        self._deal_community_cards("River", 1)
        self._run_betting_round()
        if len(self._get_active_players()) == 1:
            self._award_pot_to_winner()
            return

        # 8. Showdown
        self._handle_showdown()

        # Move dealer button for the next hand
        self.dealer_pos = (self.dealer_pos + 1) % len(self.players)

    def _run_betting_round(self):
        """Manages a full round of betting."""
        active_players = self._get_active_players()
        if not active_players: return

        # Pre-flop starts left of BB, post-flop starts left of dealer
        start_pos = (self.dealer_pos + 3) % len(self.players) if not self.community_cards else (self.dealer_pos + 1) % len(self.players)

        current_bet = self.big_blind if not self.community_cards else 0
        last_raiser = None
        players_in_round = len(active_players)
        players_acted = 0

        while players_acted < players_in_round:
            player_pos = (start_pos + players_acted) % len(self.players)
            player = self.players[player_pos]

            if not player.is_active:
                players_acted +=1
                continue

            bet_to_call = current_bet - player.current_bet
            action = player.make_decision(self.community_cards, bet_to_call, self.big_blind)
            print(f"{player.name} ({player.stack}) chooses to {action}")

            if action.action_type == ActionType.FOLD:
                player.is_active = False
            elif action.action_type == ActionType.CHECK:
                pass # Only valid if bet_to_call is 0
            elif action.action_type == ActionType.CALL:
                amount = min(bet_to_call, player.stack)
                self._process_bet(player, amount)
            elif action.action_type == ActionType.BET:
                amount = min(action.amount, player.stack)
                self._process_bet(player, amount)
                current_bet = player.current_bet
                last_raiser = player
                players_in_round = len(self._get_active_players()) # Reset for players to react to new bet
                players_acted = 0 # Start the loop again from the next player
            elif action.action_type == ActionType.RAISE:
                amount = min(bet_to_call + action.amount, player.stack)
                self._process_bet(player, amount)
                current_bet = player.current_bet
                last_raiser = player
                players_in_round = len(self._get_active_players())
                players_acted = 0 # Reset for players to react to new raise

            players_acted += 1

            # If a raise happened, the original raiser must be the last to act
            if player is last_raiser:
                break

        # Reset player bets for the next round
        for p in self.players:
            p.current_bet = 0

    def _process_bet(self, player, amount):
        """Helper to move chips from player to pot."""
        player.stack -= amount
        player.current_bet += amount
        self.pot += amount

    def _reset_for_new_hand(self):
        """Resets the game state for a new hand."""
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        for player in self.players:
            player.reset_for_new_hand()

    def _get_active_players(self):
        """Returns a list of players still in the hand."""
        return [p for p in self.players if p.is_active and p.stack > 0]

    def _post_blinds(self, active_players):
        """Posts small and big blinds."""
        sb_pos = (self.dealer_pos + 1) % len(self.players)
        bb_pos = (self.dealer_pos + 2) % len(self.players)

        sb_player = self.players[sb_pos]
        sb_amount = min(self.small_blind, sb_player.stack)
        self._process_bet(sb_player, sb_amount)
        print(f"{sb_player.name} posts small blind of {sb_amount}")

        bb_player = self.players[bb_pos]
        bb_amount = min(self.big_blind, bb_player.stack)
        self._process_bet(bb_player, bb_amount)
        print(f"{bb_player.name} posts big blind of {bb_amount}")

    def _deal_hole_cards(self, active_players):
        """Deals two cards to each active player."""
        for player in active_players:
            player.hand = [self.deck.deal(), self.deck.deal()]
        # In a real game, you wouldn't print this!
        for p in active_players: print(f"Dealt {p.hand} to {p.name}")

    def _deal_community_cards(self, stage_name, num_cards):
        """Deals community cards for flop, turn, or river."""
        self.deck.deal()  # Burn a card
        new_cards = [self.deck.deal() for _ in range(num_cards)]
        self.community_cards.extend(new_cards)
        print(f"\n--- {stage_name}: {self.community_cards} --- (Pot: {self.pot})")

    def _award_pot_to_winner(self):
        """Awards the pot to the last remaining player."""
        winners = self._get_active_players()
        if len(winners) == 1:
            winner = winners[0]
            print(f"\n{winner.name} wins the pot of {self.pot}!")
            winner.stack += self.pot
            self.pot = 0

    def _handle_showdown(self):
        """Handles the showdown to determine the winner by comparing hands."""
        print("\n--- Showdown ---")
        active_players = self._get_active_players()
        if not active_players:
            return

        if len(active_players) == 1:
            self._award_pot_to_winner()
            return

        # Evaluate and store each player's best hand
        player_hands = []
        for player in active_players:
            # The Hand class automatically finds the best 5-card hand from the 7 available cards
            hand = Hand(player.hand, self.community_cards)
            player_hands.append((player, hand))
            print(f"{player.name} shows {player.hand} for a final hand of {hand.get_rank_name()}")

        # Sort players by hand strength (best hand first)
        player_hands.sort(key=lambda x: x[1], reverse=True)

        # Determine winner(s)
        best_hand = player_hands[0][1]
        winners = [ph for ph in player_hands if ph[1] == best_hand]

        # Award the pot
        if len(winners) == 1:
            winner, winning_hand = winners[0]
            print(f"\n{winner.name} wins the pot of {self.pot} with a {winning_hand.get_rank_name()}!")
            winner.stack += self.pot
        else:
            # Handle split pot
            pot_share = self.pot // len(winners)
            winner_names = ", ".join([w[0].name for w in winners])
            winning_rank_name = winners[0][1].get_rank_name()
            print(f"\nSplit pot! {winner_names} share the pot of {self.pot} with a {winning_rank_name}.")
            for winner, _ in winners:
                winner.stack += pot_share

        self.pot = 0

    def __repr__(self):
        return f"Game(players={[p.name for p in self.players]})"