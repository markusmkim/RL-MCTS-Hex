from SimWorld.hexManager import HexManager
from SimWorld.hexManager import get_next_state, print_winner, visualize_board, visualize_game
from MCTS.tree import Tree
from Agent.actor import Actor
from config import config
from tournaments import Tournaments
from random import random
from time import time
from utils import generate_training_target, save_metadata, save_kings, save_queens, read_kings, read_queens


actor = Actor(2 * (config["size"]**2 + 1),
              config["hidden_layers"],
              config["optimizer"],
              config["activation_function"],
              config["learning_rate"],
              config["loss"],
              config["epsilon"],
              config["epsilon_decay_rate"])

saved_actor_count = 0

print("Welcome to a game of Hex!")

buffer_inputs = []
buffer_targets = []
game_history = []

start_time = time()

for i in range(config["episodes"] + 1):
    game_history = []

    if config["starting_player"] == "alternate":
        starting_player = [1, 0] if i % 2 == 0 else [0, 1]
    else:
        starting_player = config["starting_player"]

    game_manager = HexManager(starting_player, config["size"])
    game_history.append(game_manager.get_state()[1])

    tree = Tree(game_manager.get_state(), actor)
    tree.root.number_of_visits = 1

    counter = 0
    while not game_manager.is_game_over():
        visits_dict, total_visits, action = tree.mcts(config["mcts_simulations"], get_next_state, config["c"])

        if random() < config["training_probability"]:
            buffer_inputs.append(game_manager.get_state()[0])
            buffer_targets.append(generate_training_target(visits_dict, total_visits, config["size"]**2))

        game_manager.execute_action(action)

        game_history.append(game_manager.get_state()[1])
        counter += 1

    if i % config["training_frequency"] == 0 and len(buffer_inputs) > 0:
        print("Buffer size:", len(buffer_inputs), len(buffer_targets))
        if config["name"] == "demo" and i % config["save_frequency"] == 0:
            actor.train_model(buffer_inputs, buffer_targets, count=saved_actor_count)
            saved_actor_count += 1
        else:
            actor.train_model(buffer_inputs, buffer_targets)
        buffer_inputs = []
        buffer_targets = []

    # game_manager.visualize_game_state()

    print("Episode:", i, " |  Starting player:  ", starting_player, "|  Winner:", game_manager.get_winner(), " |  Epsilon: ", actor.epsilon, " | Number of moves: ", counter)

    actor.decrease_epsilon()

end_time = time()
time_spent = end_time - start_time
print("Time spent on entire run:", time_spent)
print("")

# visualize_game(game_history)  # visualize last game played, hopefully a good one

tournaments = Tournaments(config)

win_rate = tournaments.run_one_vs_all(actor)
print("Win rate for last actor:", win_rate)
print("")

if saved_actor_count > 0:
    tournaments.run_topp_tournament()
else:
    if win_rate > 0.8:
        agent_name = config["name"]
        path = f"Agent/saved_networks/{agent_name}/"
        network_path = path + "network.ckpt"
        metadata_path = path + "metadata.text"  # metadata = config + win rate
        actor.save_weights(network_path)
        save_metadata(config, metadata_path, win_rate, time_spent)

        elite_win_rate = tournaments.run_elite_tournament(actor)

        if elite_win_rate > 0.5:
            # add_to_elite(config["name"], elite_win_rate)          TODO: add player to kings/queens
            print("Player was added to elites.")

    else:
        print("The player was not good enough to join the elites.")





"""
black_1 = [[2, 1, 2], [2, 1, 1], [2, 1, 2]]
black_2 = [[1, 2, 1], [1, 1, 2], [2, 1, 2]]
black_3 = [[2, 2, 2], [2, 2, 2], [2, 2, 2]]

red_1 = [[2, 2, 1], [2, 2, 2], [1, 1, 1]]
red_2 = [[1, 1, 2], [2, 2, 1], [2, 1, 2]]
red_3 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

bingo = [[2, 1, 1, 2], [1, 2, 1, 2], [1, 1, 1, 1], [2, 1, 1, 1]]

visualize_board(bingo)
"""





