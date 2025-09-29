from tyche.game import Game
from tyche.player import Player

class Simulation:
    """
    Manages running Monte Carlo simulations of Texas Hold'em games.
    """
    def __init__(self, player_configs, num_hands):
        """
        Initializes a Simulation.

        Args:
            player_configs (list): A list of dictionaries, where each dictionary
                                 defines the attributes for a player.
            num_hands (int): The number of hands to simulate.
        """
        self.player_configs = player_configs
        self.num_hands = num_hands
        self.results = {} # To store metrics later

    def run(self):
        """
        Runs the full simulation.
        """
        print(f"Starting simulation for {self.num_hands} hands...")

        players = [Player(**config) for config in self.player_configs]
        game = Game(players)

        for i in range(self.num_hands):
            print(f"--- Hand {i+1}/{self.num_hands} ---")
            game.play_hand()
            # Reset for the next hand (e.g., community cards)
            game.community_cards = []


        self.report_results()

    def report_results(self):
        """
        Prints a summary of the simulation results.
        """
        print("="*30)
        print("Simulation Complete")
        print(f"Total Hands Played: {self.num_hands}")
        # Placeholder for more detailed metrics
        print("Results tracking will be implemented later.")
        print("="*30)

    def __repr__(self):
        return (f"Simulation(players={len(self.player_configs)}, "
                f"hands={self.num_hands})")