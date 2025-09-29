from tyche.simulation import Simulation

def main():
    """
    Main function to configure and run the poker simulation.
    """
    # Define different player types based on their attributes
    player_configurations = [
        {
            "name": "Conservative Caroline",
            "aggression": 0.2,
            "knowledge": 0.8,
            "inebriation": 0.1,
            "analytics": 0.7
        },
        {
            "name": "Aggressive Adam",
            "aggression": 0.9,
            "knowledge": 0.5,
            "inebriation": 0.4,
            "analytics": 0.4
        },
        {
            "name": "Newbie Nate",
            "aggression": 0.5,
            "knowledge": 0.2,
            "inebriation": 0.2,
            "analytics": 0.1
        },
        {
            "name": "Drunk Diana",
            "aggression": 0.7,
            "knowledge": 0.3,
            "inebriation": 0.9,
            "analytics": 0.2
        },
    ]

    # Configure the simulation
    num_hands_to_simulate = 5

    # Create and run the simulation
    simulation = Simulation(
        player_configs=player_configurations,
        num_hands=num_hands_to_simulate
    )
    simulation.run()

if __name__ == "__main__":
    main()