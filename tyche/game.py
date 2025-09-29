from tyche.card import Deck
from tyche.player import Player
from tyche.action import Action, ActionType
from tyche.hand import Hand

class Game:
    """
    Represents and manages a single game of Texas Hold'em.
    This class is designed to run "quietly" and return results.
    """
    def __init__(self, players, small_blind=5, big_blind=10):
        self.players = players
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.dealer_pos = 0

    def play_hand(self):
        """
        Plays one complete hand of Texas Hold'em and returns the result.
        """
        self._reset_for_new_hand()
        active_players = self._get_active_players()
        if len(active_players) < 2:
            return None # Not enough players

        self._post_blinds()
        self._deal_hole_cards()

        # Run betting rounds for each stage of the game
        for stage in ["preflop", "flop", "turn", "river"]:
            if len(self._get_active_players()) > 1:
                if stage != "preflop":
                    self._deal_community_cards(3 if stage == "flop" else 1)
                self._run_betting_round()

        # Determine the outcome
        final_players = self._get_active_players()
        if len(final_players) == 1:
            result = self._award_pot_to_last_player(final_players[0])
        else:
            result = self._handle_showdown(final_players)

        # Update player stacks based on the result
        winners = [p for p in self.players if p.name in result['winners']]
        if winners:
            pot_share = self.pot // len(winners)
            for winner in winners:
                winner.stack += pot_share

        # Move dealer button for the next hand
        self.dealer_pos = (self.dealer_pos + 1) % len(self.players)

        return result

    def _run_betting_round(self):
        active_players = self._get_active_players()
        if not active_players or len(active_players) == 1: return

        start_pos = (self.dealer_pos + 3) % len(self.players) if not self.community_cards else (self.dealer_pos + 1) % len(self.players)

        # Find the first active player to start the action
        while not self.players[start_pos].is_active:
            start_pos = (start_pos + 1) % len(self.players)

        current_bet = max(p.current_bet for p in self.players)
        last_raiser = None
        action_count = 0

        player_index = start_pos

        while action_count < len(active_players):
            player = self.players[player_index]

            if player.is_active:
                if player is last_raiser: # Full circle after a raise, round ends
                    break

                bet_to_call = current_bet - player.current_bet
                action = player.make_decision(self.community_cards, bet_to_call, self.big_blind)

                is_aggressive_action = False
                if action.action_type == ActionType.FOLD:
                    player.is_active = False
                elif action.action_type == ActionType.CALL:
                    self._process_bet(player, bet_to_call)
                elif action.action_type == ActionType.BET:
                    self._process_bet(player, action.amount)
                    current_bet = player.current_bet
                    last_raiser = player
                    is_aggressive_action = True
                elif action.action_type == ActionType.RAISE:
                    # Amount to process is the call amount + the raise amount
                    self._process_bet(player, bet_to_call + action.amount)
                    current_bet = player.current_bet
                    last_raiser = player
                    is_aggressive_action = True

                if is_aggressive_action:
                    action_count = 0 # Reset so everyone gets to act again

            action_count += 1
            player_index = (player_index + 1) % len(self.players)

        # Reset player bets for the next street
        for p in self.players: p.current_bet = 0

    def _process_bet(self, player, amount):
        actual_amount = min(amount, player.stack)
        player.stack -= actual_amount
        player.current_bet += actual_amount
        self.pot += actual_amount

    def _reset_for_new_hand(self):
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        for player in self.players:
            player.reset_for_new_hand()

    def _get_active_players(self):
        return [p for p in self.players if p.is_active and p.stack > 0]

    def _post_blinds(self):
        sb_pos = (self.dealer_pos + 1) % len(self.players)
        while not self.players[sb_pos].is_active: sb_pos = (sb_pos + 1) % len(self.players)

        bb_pos = (sb_pos + 1) % len(self.players)
        while not self.players[bb_pos].is_active: bb_pos = (bb_pos + 1) % len(self.players)

        sb_player = self.players[sb_pos]
        self._process_bet(sb_player, self.small_blind)

        bb_player = self.players[bb_pos]
        self._process_bet(bb_player, self.big_blind)

    def _deal_hole_cards(self):
        for player in self._get_active_players():
            player.hand = [self.deck.deal(), self.deck.deal()]

    def _deal_community_cards(self, num_cards):
        self.deck.deal()  # Burn a card
        self.community_cards.extend([self.deck.deal() for _ in range(num_cards)])

    def _award_pot_to_last_player(self, winner):
        return {
            "winners": [winner.name],
            "winning_hand": "Folds",
            "pot": self.pot
        }

    def _handle_showdown(self, active_players):
        player_hands = []
        for player in active_players:
            hand = Hand(player.hand, self.community_cards)
            player_hands.append((player, hand))

        player_hands.sort(key=lambda x: x[1], reverse=True)
        best_hand = player_hands[0][1]
        winners = [ph[0] for ph in player_hands if ph[1] == best_hand]

        return {
            "winners": [w.name for w in winners],
            "winning_hand": best_hand.get_rank_name(),
            "pot": self.pot
        }

    def __repr__(self):
        return f"Game(players={[p.name for p in self.players]})"