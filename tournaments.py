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
            player = Actor(0, 0, count=i)  # demo models
            # player.load_weights(f"Agent/saved_networks/demo/cp-{i}.ckpt")
            players.append(player)

        for i in range(randoms):
            players.append(Actor(1, 1,
                                 input_dim=2 * (self.config["size"] ** 2 + 1),
                                 hidden_layers=self.config["hidden_layers"],
                                 activation_function=self.config["activation_function"]))

        print("TOPP tournament is over. The 4 last players take random actions.")
        number_of_wins, number_of_games, detailed_stats = self.play_tournament_games(players)
        print_stats(number_of_wins, number_of_games, detailed_stats)


    def run_one_vs_all(self, actor, randoms=19):
        print("Running one vs all")
        players = [actor]

        for i in range(randoms):
            players.append(Actor(1, 1,
                                 input_dim=2 * (self.config["size"] ** 2 + 1),
                                 hidden_layers=self.config["hidden_layers"],
                                 activation_function=self.config["activation_function"]))

        number_of_wins, number_of_games, detailed_stats = self.play_tournament_games(players)
        print("OneVsAll tournament is over. Only the first player is trained.")
        print_stats(number_of_wins, number_of_games, detailed_stats)

        return number_of_wins[0] / number_of_games[0]


    def run_elite_tournament(self, actor=None):
        print("Running elite tournament")
        names = [key for key in read_queens()] + [key for key in read_kings()]
        if names is None or len(names) == 0:
            print('No elites to play against')
            return -1

        players = [actor] if actor else []
        for i in range(len(names)):
            player = Actor(0, 0, name=names[i])
            players.append(player)

        number_of_wins, number_of_games, detailed_stats = self.play_tournament_games(players)
        if actor:
            print("Elite tournament is over. The first player is new.")
            names.insert(0, "New Player")
            print("All players:", names)
        else:
            print("Elite tournament is over.")
            print("All players:", names)

        print_stats(number_of_wins, number_of_games, detailed_stats)

        return number_of_wins[0] / number_of_games[0] if actor else None


    def evaluate_actor(self, actor):
        win_rate_one_vs_all = self.run_one_vs_all(actor, randoms=9)
        win_rate_elite = self.run_elite_tournament(actor=actor)
        if win_rate_elite == -1:
            return win_rate_one_vs_all
        return win_rate_one_vs_all * 0.2 + win_rate_elite * 0.8


    def run_interaction_game(self, actor, actor_starts=False):
        starting_player = [1, 0] if not actor_starts else [0, 1]
        game_manager = HexManager(starting_player, self.config["size"])
        game_manager.visualize_game_state()
        while not game_manager.is_game_over():
            if game_manager.get_state()[0][0] == 1:
                action = -1
                while action not in game_manager.get_state()[2]:
                    action = int(input("Action: "))
            else:
                action = actor.find_best_action(game_manager.get_state())
            game_manager.execute_action(action)
            game_manager.visualize_game_state()
        winner = game_manager.get_winner()
        print("Winner:", winner)


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
