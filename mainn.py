from SimWorld.hexManager import HexManager
from SimWorld.hexManager import get_next_state, print_winner, visualize_board, visualize_game
from MCTS.tree import Tree
from Agent.actor import Actor
from config import config
from tournaments import Tournaments
from random import random
from time import time
from utils import generate_training_target, save_metadata, save_kings, save_queens, read_kings, read_queens, plot_history

# --------------------------------------
elite_group = "queens"  # kings | queens
train_from = "hermine"       # name or None
run_interaction_game = False
# --------------------------------------

if train_from:
    actor = Actor(config["epsilon"], config["epsilon_decay_rate"], name=train_from)

else:
    actor = Actor(config["epsilon"],
                  config["epsilon_decay_rate"],
                  input_dim=2 * (config["size"]**2 + 1),
                  hidden_layers=config["hidden_layers"],
                  optimizer=config["optimizer"],
                  activation_function=config["activation_function"],
                  learning_rate=config["learning_rate"],
                  loss=config["loss"])

saved_actor_count = 0

print("Welcome to a game of Hex!")

buffer_inputs = []
buffer_targets = []
game_history = []

start_time = time()

evaluation_history = []
best_evaluation = 0

tournaments = Tournaments(config)

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

    simulations = config["mcts_simulations"]
    counter = 0
    while not game_manager.is_game_over():

        if random() < config["training_probability"]:
            visits_dict, total_visits, action = tree.mcts(simulations, get_next_state, config["c"])
            buffer_inputs.append(game_manager.get_state()[0])
            buffer_targets.append(generate_training_target(visits_dict, total_visits, config["size"]**2))
        else:
            visits_dict, total_visits, action = tree.mcts(config["mcts_discounted_simulations"], get_next_state, config["c"])

        if len(buffer_inputs) == config["buffer_size"]:
            break

        game_manager.execute_action(action)

        game_history.append(game_manager.get_state()[1])

        simulations -= config["mcts_discount_constant"]
        counter += 1

    if len(buffer_inputs) == config["buffer_size"]:
        print("Training actor network | Buffer size:", len(buffer_inputs))
        actor.train_model(buffer_inputs, buffer_targets, config["batch_size"], config["epochs"])
        buffer_inputs = []
        buffer_targets = []

    if i % config["save_frequency"] == 0:
        if config["name"] == "demo":
            print("Saving network")
            actor.save_model("demo", saved_actor_count)
            saved_actor_count += 1
        elif i > 0:
            evaluation = tournaments.evaluate_actor(actor)
            evaluation_history.append(evaluation)
            actor.save_model("last_model")
            print("Intermediate evaluation:", evaluation)
            if evaluation > best_evaluation:
                best_evaluation = evaluation
                actor.save_model("best_model_last_run")
                print("Evaluation record so far in this run!")

    print("Episode:", i, " |  Starting player:  ", starting_player, " |  Winner:", game_manager.get_winner(), " |  Epsilon: ", actor.epsilon, " | Number of moves: ", counter)

    actor.decrease_epsilon()

end_time = time()
time_spent = end_time - start_time
print("Time spent on entire run:", time_spent)
if len(evaluation_history) > 0:
    plot_history(evaluation_history, config["save_frequency"])
print("")
# visualize_game(game_history)  # visualize last game played, hopefully a good one

print("Setting actor epsilon = 0")
actor.epsilon = 0

if run_interaction_game:
    tournaments.run_interaction_game(actor, actor_starts=True)

if saved_actor_count > 0:
    win_rate = tournaments.run_one_vs_all(actor)
    print("Win rate for last actor:", win_rate)
    print("")
    tournaments.run_topp_tournament()
else:
    evaluation = tournaments.evaluate_actor(actor)
    print("Evaluation:", evaluation)
    actor.save_model(config["name"])
    save_metadata(config, evaluation, time_spent)
    if evaluation > 0.5:
        if elite_group == "queens":
            queens = read_queens()
            queens[config["name"]] = evaluation   # win rate against randoms
            save_queens(queens)             # if agent was already in queens, win rate is overwritten
            print("Player was added to queens.")

        if elite_group == "kings":
            kings = read_kings()
            kings[config["name"]] = evaluation
            save_kings(kings)
            print("Player was added to kings.")
    else:
        print("The player was not good enough to join the elites.")


