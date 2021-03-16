from SimWorld.hexManager import HexManager
from SimWorld.hexManager import get_next_state
from MCTS.tree import Tree
from Agent.actor import Actor
# from time import sleep  # |  sleep(0.5) --> 0.5 sec
from math import sqrt
import numpy as np


def generate_training_target(visits_dict, total_visits, size):
    training_target = []
    for k in range(size):
        if k in visits_dict:
            training_target.append(visits_dict[k] / total_visits)
        else:
            training_target.append(0)
    return training_target


def generate_training_input(game_state):
    training_input = [int(game_state[0] == 0), int(game_state[0] == 1)]
    return np.concatenate((training_input, game_state[1]))


actor = Actor(34, [50, 10], 0.001, 0.5, 0.999)

print("")
print("Welcome to a game of Hex!")
print("")

episodes = 1
wins_for_player_0 = 0

for i in range(episodes):
    print("Episode:", i)

    game_manager = HexManager(0, 4)
    tree = Tree(game_manager.get_state(), actor)
    tree.root.number_of_visits = 1

    buffer_inputs = []
    buffer_targets = []

    while not game_manager.is_game_over():
        # print("States:")
        # print("Root state:", tree.root.state)
        # print("Game state:", game_manager.get_state())
        visits_dict, total_visits, action = tree.mcts(1000, get_next_state)
        print("noob")

        buffer_inputs.append(generate_training_input(game_manager.get_state()[:-1]))
        buffer_targets.append(generate_training_target(visits_dict, total_visits, len(game_manager.grid) // 2))

        # print("Action:", action)
        game_manager.execute_action(action)

    print("Winner:", game_manager.get_winner())

    if game_manager.get_winner() == 0:
        wins_for_player_0 += 1

    # if last episode
    if i == episodes - 1:
        game_manager.visualize_game()


print("Win rate for player 0:", wins_for_player_0 / episodes)




"""
game_manager = HexManager(0, 3)
tree = Tree(game_manager.get_state())
tree.root.number_of_visits = 1

black_1 = [[0, 1, 0], [0, 1, 1], [0, 1, 0]]
black_2 = [[1, 0, 1], [1, 1, 0], [0, 1, 0]]
black_3 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

red_1 = [[0, 0, 1], [0, 0, 0], [1, 1, 1]]
red_2 = [[1, 1, 0], [0, 0, 1], [0, 1, 0]]
red_3 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

bingo = [[1, 1, 1], [0, 0, 1], [1, 1, 1]]

game_manager.visualize_board(black_1)
game_manager.print_winner(black_1)
game_manager.print_winner(black_2)
game_manager.print_winner(black_3)

game_manager.print_winner(red_1)
game_manager.print_winner(red_2)
game_manager.print_winner(red_3)
"""
