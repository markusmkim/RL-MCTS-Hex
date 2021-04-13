from Agent.actor import Actor
from SimWorld.hexManager import HexManager
import numpy as np
from Main.utils import read_queens, read_kings, save_queens, save_kings
from Tournaments.utils import print_stats, plot_stats


class Tournaments:
    def __init__(self, config):
        self.config = config


    def run_topp_tournament(self, randoms=0, plot=False):
        print("Running TOPP tournament")
        randoms = randoms
        number_of_actors = int(self.config["episodes"] / self.config["save_frequency"]) + 1
        players = []

        for i in range(number_of_actors):
            player = Actor(0, 0, count=i)  # bestDemo models
            players.append(player)

        for i in range(randoms):
            players.append(Actor(1, 1,
                                 input_dim=2 * (self.config["size"] ** 2 + 1),
                                 hidden_layers=self.config["actor_hidden_layers"],
                                 activation=self.config["actor_activation"]))

        number_of_wins, number_of_games, detailed_stats = self.play_tournament_games(players)
        print("TOPP tournament is over. The", randoms, "last players take random actions.")
        print_stats(number_of_wins, number_of_games, detailed_stats)
        if plot:
            plot_stats(number_of_wins, np.arange(0, self.config["episodes"] + 1, self.config["save_frequency"]))


    def run_one_vs_all(self, actor, randoms=19, display=True):
        if display:
            print("Running one vs all")
        players = [actor]

        for i in range(randoms):
            players.append(Actor(1, 1,
                                 input_dim=2 * (self.config["size"] ** 2 + 1),
                                 hidden_layers=self.config["actor_hidden_layers"],
                                 activation=self.config["actor_activation"]))

        number_of_wins, number_of_games, detailed_stats = self.play_tournament_games(players)

        if display:
            print("OneVsAll tournament is over. Only the first player is trained.")
            print_stats(number_of_wins, number_of_games, detailed_stats)

        return number_of_wins[0] / number_of_games[0]


    def run_elite_tournament(self, actor=None, names=None, randoms=0, update=False, display=True):
        if display:
            print("Running elite tournament")
        if names is None:
            names = [key for key in read_queens()] + [key for key in read_kings()]
            if names is None or len(names) == 0:
                if display:
                    print('No elites to play against')
                return -1

        players = [actor] if actor else []
        for i in range(len(names)):
            player = Actor(0, 0, name=names[i])
            players.append(player)

        for i in range(randoms):
            names.append("random")
            players.append(Actor(1, 1,
                                 input_dim=2 * (self.config["size"] ** 2 + 1),
                                 hidden_layers=self.config["actor_hidden_layers"],
                                 activation=self.config["actor_activation"]))

        number_of_wins, number_of_games, detailed_stats = self.play_tournament_games(players)

        if update:
            return names, number_of_wins, number_of_games

        if display:
            if actor:
                print("Elite tournament is over. The first player is new.")
                names.insert(0, "New Player")
                print("All players:", names)
            else:
                print("Elite tournament is over.")
                print("All players:", names)

            if randoms > 0:
                print("The last", randoms, "players take random actions.")

            print_stats(number_of_wins, number_of_games, detailed_stats)

        return number_of_wins[0] / number_of_games[0] if actor else None


    def update_elite_evaluations(self):
        print(" --- Updating elite evaluations --- ")
        names, number_of_wins, number_of_games = self.run_elite_tournament(update=True)

        queens = read_queens()
        kings = read_kings()

        for i in range(len(names)):
            actor = Actor(0, 0, name=names[i])
            win_rate = self.run_one_vs_all(actor, randoms=9, display=False)
            elite_win_rate = number_of_wins[i] / number_of_games[i]
            evaluation = 0.5 * win_rate + 0.5 * elite_win_rate
            if names[i] in queens:
                queens[names[i]] = evaluation
            else:
                kings[names[i]] = evaluation

        save_queens(queens)
        save_kings(kings)


    def evaluate_actor(self, actor, display=True):
        win_rate_one_vs_all = self.run_one_vs_all(actor, randoms=19, display=display)
        if not display:
            print("Win rate one vs all:", win_rate_one_vs_all)
        win_rate_elite = self.run_elite_tournament(actor=actor, display=display)
        if win_rate_elite == -1:
            return win_rate_one_vs_all
        return win_rate_one_vs_all * 0.5 + win_rate_elite * 0.5


    def run_interaction_game(self, actor, actor_starts=False, critic=None):
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
            if critic:
                print(critic.evaluate(game_manager.get_state()).numpy()[0])
        winner = game_manager.get_winner()
        print("Winner:", winner)


    def play_tournament_games(self, players):
        number_of_players = len(players)
        number_of_games = np.zeros(number_of_players)
        number_of_wins = np.zeros(number_of_players)
        detailed_stats = np.zeros((number_of_players, number_of_players))

        for i in range(number_of_players - 1):
            for j in range(i + 1, number_of_players):

                half = self.config["tournament_games"] // 2

                for n in range(self.config["tournament_games"]):
                    number_of_games[i] += 1
                    number_of_games[j] += 1

                    first_player = i if n >= half else j
                    second_player = j if n >= half else i

                    player1 = players[first_player]  # [1, 0]
                    player2 = players[second_player]  # [0, 1]

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
                        number_of_wins[first_player] += 1
                        detailed_stats[first_player][second_player] += 1
                    else:
                        number_of_wins[second_player] += 1
                        detailed_stats[second_player][first_player] += 1

        return number_of_wins, number_of_games, detailed_stats
