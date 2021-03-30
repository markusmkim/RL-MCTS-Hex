from Agent.actor import Actor
from SimWorld.hexManager import HexManager
import numpy as np
from utils import read_queens, read_kings


class Tournaments:
    def __init__(self, config):
        self.config = config


    def run_topp_tournament(self):
        print("Running TOPP tournament")
        randoms = 4
        number_of_actors = int(self.config["episodes"] / self.config["save_frequency"]) + 1
        players = []

        for i in range(number_of_actors):
            player = Actor(2 * (self.config["size"] ** 2 + 1),
                           self.config["hidden_layers"],
                           None, self.config["activation_function"], 0, None, 0, 0)
            player.load_weights(f"Agent/saved_networks/demo/cp-{i}.ckpt")
            players.append(player)

        for i in range(randoms):
            players.append(Actor(2 * (self.config["size"] ** 2 + 1),
                               self.config["hidden_layers"],
                               None, self.config["activation_function"], 0, None, 1, 1))

        print("TOPP tournament is over. The 4 last players take random actions.")
        number_of_wins, number_of_games, detailed_stats = self.play_tournament_games(players)
        print_stats(number_of_wins, number_of_games, detailed_stats)


    def run_one_vs_all(self, actor):
        print("Running one vs all")
        randoms = 19
        players = [actor]

        for i in range(randoms):
            players.append(Actor(2 * (self.config["size"] ** 2 + 1),
                           self.config["hidden_layers"],
                           None, self.config["activation_function"], 0, None, 1, 1))

        number_of_wins, number_of_games, detailed_stats = self.play_tournament_games(players)
        print("OneVsAll tournament is over. Only the first player is trained.")
        print_stats(number_of_wins, number_of_games, detailed_stats)

        return number_of_wins[0] / number_of_games[0]


    def run_elite_tournament(self, actor):
        print("Running elite tournament")
        names = [key for key in read_queens()] + [key for key in read_kings()]
        if names is None or len(names) == 0:
            print('No elites to play against')
            return 1  # win rate is 1 if only player
        players = [actor]
        for i in range(len(names)):
            player = Actor(2 * (self.config["size"] ** 2 + 1),
                           self.config["hidden_layers"],
                           None, self.config["activation_function"], 0, None, 0, 0)
            player.load_weights(f"Agent/saved_networks/{names[i]}/network.ckpt")
            players.append(player)

        number_of_wins, number_of_games, detailed_stats = self.play_tournament_games(players)
        print("Elite tournament is over. The first player is new.")
        print("All players:", names.insert(0, "New Player"))
        print_stats(number_of_wins, number_of_games, detailed_stats)

        return number_of_wins[0] / number_of_games[0]


    def play_tournament_games(self, players):
        number_of_players = len(players)
        number_of_games = np.zeros(number_of_players)
        number_of_wins = np.zeros(number_of_players)
        detailed_stats = np.zeros((number_of_players, number_of_players))

        for i in range(number_of_players - 1):
            for j in range(i + 1, number_of_players):
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
                        detailed_stats[i][j] += 1
                    else:
                        number_of_wins[j] += 1
                        detailed_stats[j][i] += 1

        return number_of_wins, number_of_games, detailed_stats


def print_stats(stats, games, detailed_stats):
    print("")
    print("Stats:")
    print(stats)
    print("")
    print("Number of games:")
    print(games)
    print("")
    print("Detailed stats:")
    print(detailed_stats)
    print("")
