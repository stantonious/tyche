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
        self.results = [] # Stores the results dictionary from each hand

    def run(self):
        """
        Runs the full simulation and collects the results.
        """
        print(f"Running simulation for {self.num_hands} hands...")
        players = [Player(**config) for config in self.player_configs]
        game = Game(players)

        for _ in range(self.num_hands):
            result = game.play_hand()
            if result:
                self.results.append(result)

        self.report_results()

    def report_results(self):
        """
        Prints a summary of the simulation results in a clean, tabular format.
        """
        from tabulate import tabulate
        from collections import Counter

        print("\n" + "="*15 + " Hand-by-Hand Results " + "="*15)

        # Prepare data for the hand results table
        headers = ["Hand #", "Winner(s)", "Winning Hand", "Pot Size"]
        table_data = []
        for i, result in enumerate(self.results):
            winner_str = ", ".join(result['winners'])
            table_data.append([
                i + 1,
                winner_str,
                result['winning_hand'],
                result['pot']
            ])

        print(tabulate(table_data, headers=headers, tablefmt="grid"))

        # Prepare data for the summary table
        print("\n" + "="*17 + " Final Standings " + "="*17)
        all_winners = [winner for result in self.results for winner in result['winners']]
        win_counts = Counter(all_winners)

        summary_headers = ["Player", "Hands Won"]
        summary_data = []
        for player_config in self.player_configs:
            name = player_config['name']
            summary_data.append([name, win_counts.get(name, 0)])

        # Sort by hands won
        summary_data.sort(key=lambda x: x[1], reverse=True)

        print(tabulate(summary_data, headers=summary_headers, tablefmt="grid"))

    def __repr__(self):
        return (f"Simulation(players={len(self.player_configs)}, "
                f"hands={self.num_hands})")