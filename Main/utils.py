import matplotlib.pyplot as plt
import numpy as np
from random import random
from MCTS.tree import Tree
from Agent.actor import Actor
from Agent.critic import Critic
from SimWorld.hexManager import HexManager, get_next_state


def generate_training_target(visits_dict, total_visits, size):
    training_target = []
    for k in range(size):
        if k in visits_dict:
            training_target.append(visits_dict[k] / total_visits)
        else:
            training_target.append(0)
    return training_target


def train_actor(actor, critic, config, tournaments, rollout_actor):
    print("Training models...")

    evaluation_history = []
    best_evaluation = 0
    saved_actor_count = 0
    buffer_inputs = []
    buffer_targets = []
    red_buffer_inputs = []
    red_buffer_targets = []
    black_buffer_inputs = []
    black_buffer_targets = []
    last_game_history = []

    rollout_prob = config["rollout_prob"]

    for i in range(config["episodes"] + 1):
        starting_player = [1, 0] if i % 2 == 0 else [0, 1]
        game_manager = HexManager(starting_player, config["size"])

        if i == config["episodes"]:
            last_game_history.append(game_manager.get_state()[1])

        tree = Tree(game_manager.get_state(), actor, critic)
        if rollout_actor:
            if i < config["episodes"] // 2:
                tree = Tree(game_manager.get_state(), rollout_actor, critic)
        tree.root.number_of_visits = 1

        simulations = config["mcts_simulations"]
        number_of_moves = 0
        while not game_manager.is_game_over():
            if random() < config["training_probability"]:
                visits_dict, total_visits, action, critic_input_buffer, critic_target_buffer = tree.mcts(
                    simulations,
                    get_next_state,
                    config["c"],
                    rollout_prob)

                if actor.akimbo:
                    if game_manager.get_state()[0][1]:  # black to move
                        black_buffer_inputs.append(game_manager.get_state()[0][2:])
                        black_buffer_targets.append(
                            generate_training_target(visits_dict, total_visits, config["size"] ** 2))
                    else:
                        red_buffer_inputs.append(game_manager.get_state()[0][2:])
                        red_buffer_targets.append(
                            generate_training_target(visits_dict, total_visits, config["size"] ** 2))

                else:
                    buffer_inputs.append(game_manager.get_state()[0])
                    buffer_targets.append(generate_training_target(visits_dict, total_visits, config["size"] ** 2))
            else:
                visits_dict, total_visits, action, critic_input_buffer, critic_target_buffer = tree.mcts(
                    config["mcts_discounted_simulations"],
                    get_next_state,
                    config["c"], rollout_prob)

            if len(buffer_inputs) == config["buffer_size"]:
                print("Training actor network | Buffer size:", len(buffer_inputs))
                actor.train_model(buffer_inputs, buffer_targets, config["batch_size"], config["epochs"])
                buffer_inputs = []
                buffer_targets = []

            if actor.akimbo:
                if len(black_buffer_inputs) == config["buffer_size"]:
                    print("Training akimboActors black network | Buffer size:", len(black_buffer_inputs))
                    actor.train_model(black_buffer_inputs, black_buffer_targets, config["batch_size"], config["epochs"], color=1)
                    black_buffer_inputs = []
                    black_buffer_targets = []

                if len(red_buffer_inputs) == config["buffer_size"]:
                    print("Training akimboActors red network | Buffer size:", len(red_buffer_inputs))
                    actor.train_model(red_buffer_inputs, red_buffer_targets, config["batch_size"], config["epochs"], color=2)
                    red_buffer_inputs = []
                    red_buffer_targets = []

            game_manager.execute_action(action)

            if i == config["episodes"]:
                last_game_history.append(game_manager.get_state()[1])

            if len(critic_input_buffer) > 8:
                critic.train_model(critic_input_buffer, critic_target_buffer, config["batch_size"], config["epochs"])

            simulations -= config["mcts_discount_constant"]
            number_of_moves += 1

        if i % config["save_frequency"] == 0:
            if config["name"] == "demo":
                print("Saving network")
                actor.save_model("demo", saved_actor_count)
                saved_actor_count += 1
            elif i > 0:
                if config["size"] == 6:
                    evaluation = tournaments.evaluate_actor(actor, display=False)
                else:
                    evaluation = tournaments.run_one_vs_all(actor, 9, display=False)
                evaluation_history.append(evaluation)
                actor.save_model("last_model")
                print("Intermediate evaluation:", evaluation)
                if evaluation > best_evaluation:
                    best_evaluation = evaluation
                    actor.save_model("best_model_last_run")
                    print("Best evaluation so far this run!")

        print("Episode:", i,
              " |  Starting player:  ", starting_player,
              " |  Winner:", game_manager.get_winner(),
              " |  Epsilon: ", actor.epsilon,
              " |  Rollout prob", rollout_prob,
              " |  Number of moves: ", number_of_moves)

        actor.decrease_epsilon()
        rollout_prob = rollout_prob * config["rollout_prob_decay_rate"]

    return evaluation_history, last_game_history, saved_actor_count


def initialize_actor(config, train_from, akimbo):
    if train_from:
        return Actor(config["epsilon"], config["epsilon_decay_rate"], name=train_from, akimbo=akimbo)
    return Actor(config["epsilon"],
                 config["epsilon_decay_rate"],
                 input_dim=2 * (config["size"] ** 2 + 1),
                 hidden_layers=config["hidden_layers"],
                 optimizer=config["optimizer"],
                 activation=config["activation"],
                 learning_rate=config["learning_rate"],
                 l2_reg=config["l2_reg"],
                 loss=config["loss"],
                 akimbo=akimbo)


def initialize_critic(config):
    return Critic(input_dim=2 * (config["size"] ** 2 + 1),
                  hidden_layers=config["hidden_layers"],
                  optimizer=config["optimizer"],
                  activation=config["activation"],
                  learning_rate=config["learning_rate"],
                  l2_reg=config["l2_reg"],
                  loss=config["loss"])


def plot_history(history, frequency):
    x_axis = np.arange(len(history))
    x_axis = x_axis * frequency
    plt.plot(x_axis, history)
    plt.show()


def save_metadata(config, evaluation, time_spent):
    name = config["name"]
    filepath = f"Agent/saved_models/{name}/metadata.text"  # metadata = config + win rate
    data = [f"{key}: {config[key]}" for key in config]
    file = open(filepath, "w")  # w = overwrite if already exists
    [file.write(line + "\n") for line in data]
    file.write("\nEvaluation: " + str(evaluation))
    file.write("\nTime spent: " + str(time_spent))
    file.close()


def read_kings():
    path = "Agent/saved_models/kings.txt"
    return read_royalty(path)


def read_queens():
    path = "Agent/saved_models/queens.txt"
    return read_royalty(path)


def read_royalty(filepath):
    data = {}
    file = open(filepath, "r")
    try:
        for line in file.readlines():
            name_score = line.split(": ")
            if len(name_score) == 2:
                data[name_score[0]] = name_score[1].rstrip()
    finally:
        file.close()
    return data


def save_kings(data):
    """
    :param data: Dictionary of type {name: win_rate}
    """
    path = "Agent/saved_models/kings.txt"
    save_royalty(path, data)


def save_queens(data):
    """
    :param data: Dictionary of type {name: win_rate}
    """
    path = "Agent/saved_models/queens.txt"
    save_royalty(path, data)


def save_royalty(filepath, data):
    file = open(filepath, "w")
    try:
        data = [f"{key}: {data[key]}" for key in data]
        [file.write(line + "\n") for line in data]
    finally:
        file.close()
