from Agent.actor import Actor
from SimWorld.hexManager import HexManager


class OneVsAll:
    def __init__(self, config):
        self.config = config

    def run_one_vs_all(self, actor):
        randoms = 9

        print("Running one vs all")
        players = []
        number_of_games = []
        number_of_wins = []
        # detailed_stats = np.zeros((number_of_actors, number_of_actors))
        for i in range(randoms):
            player = Actor(2 * (self.config["size"] ** 2 + 1),
                           self.config["hidden_layers"],
                           None, self.config["activation_function"], 0, 1, 1)
            players.append(player)
            number_of_wins.append(0)
            number_of_games.append(0)

        players.append(actor)
        number_of_wins.append(0)
        number_of_games.append(0)

        for i in range(len(players) - 1):
            for j in range(i + 1, len(players)):
                print("Games...")
                for n in range(self.config["TOPP-G"]):
                    number_of_games[i] += 1
                    number_of_games[j] += 1
                    player1 = players[i]  # [1, 0]
                    player2 = players[j]  # [0, 1]
                    starting_player = [1, 0] if n % 2 == 0 else [0, 1]

                    game_manager = HexManager(starting_player, self.config["size"])

                    while not game_manager.is_game_over():
                        if game_manager.get_state()[0][0] == 1:
                            action = player1.find_best_action(game_manager.get_state())
                        else:
                            action = player2.find_best_action(game_manager.get_state())
                        game_manager.execute_action(action)

                    winner = game_manager.get_winner()
                    if winner == 1:
                        number_of_wins[i] += 1
                        # detailed_stats[i][j] += 1
                    else:
                        number_of_wins[j] += 1
                        # detailed_stats[j][i] += 1

        print("One vs all tournament over")
        print("Stats: ", number_of_wins)
        print("number of games", number_of_games)
        print("Detailed")
        # print(detailed_stats)
