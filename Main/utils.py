import matplotlib.pyplot as plt
import numpy as np
from random import randrange
from MCTS.tree import Tree
from Agent.actor import Actor
from Agent.critic import Critic
from SimWorld.hexManager import HexManager, get_next_state
from time import time


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

    buffer_inputs = []
    buffer_targets = []

    buffer = {}

    last_game_history = []
    evaluation_history = []

    best_evaluation = 0
    saved_actor_count = 0

    rollout_prob = config["rollout_prob"]
    total_rollout_prob = config["min_rollout_prob"] + rollout_prob

    """ Time-stuff """
    last_save_start_time = time()
    time_history = []

    if rollout_actor:
        rollout_actor = initialize_actor(config, rollout_actor)

    for i in range(config["episodes"] + 1):
        starting_player = [1, 0] if i % 2 == 0 else [0, 1]
        game_manager = HexManager(starting_player, config["size"])

        if i == config["episodes"]:
            last_game_history.append(game_manager.get_state()[1])

        tree = Tree(game_manager.get_state(), actor, critic)
        if rollout_actor:
            if i < 100:
                tree = Tree(game_manager.get_state(), rollout_actor, critic)
        tree.root.number_of_visits = 1

        number_of_moves = 0
        simulations = config["mcts_starting_simulations"]

        while not game_manager.is_game_over():
            visits_dict, total_visits, action, critic_input_buffer, critic_target_buffer = tree.mcts(
                simulations,
                get_next_state,
                config["c"],
                total_rollout_prob)

            buffer_inputs.append(game_manager.get_state()[0])
            buffer_targets.append(generate_training_target(visits_dict, total_visits, config["size"] ** 2))

            game_manager.execute_action(action)

            if i == config["episodes"]:
                last_game_history.append(game_manager.get_state()[1])

            if len(critic_input_buffer) > 8:
                critic.train_model(critic_input_buffer, critic_target_buffer, config["batch_size"], config["epochs"])

            if number_of_moves > config["mcts_move_increase"]:
                if number_of_moves > config["mcts_move_decrease"]:
                    simulations -= config["mcts_decrease_constant"]
                else:
                    simulations += config["mcts_increase_constant"]
            number_of_moves += 1

        old_buffer_size = len(buffer)

        train_network(actor, buffer, buffer_inputs, buffer_targets, config)

        buffer_inputs = []
        buffer_targets = []

        if i % config["save_frequency"] == 0:
            print("Saving network")

            """ Time-stuff """
            if i > 0:
                time_spent_on_save = time() - last_save_start_time
                time_history.append(time_spent_on_save)
                if len(time_history) > 1:
                    time_spent_on_last_save = time_history[-2]
                    ratio = time_spent_on_save / time_spent_on_last_save
                    print("Time spent on current save:  ", time_spent_on_save)
                    print("Time spent on previous save: ", time_spent_on_last_save)
                    print("Ratio:", ratio)
                    print("Time history:", time_history)
                else:
                    print("Time spent on first save:", time_spent_on_save)

            if config["name"] == "demo":
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

            last_save_start_time = time()

        print("Episode:", i,
              " |  Starting player: ", starting_player,
              " |  Winner: ", game_manager.get_winner(),
              " |  Epsilon: ", actor.epsilon,
              " |  Rollout prob: ", "{:.3f}".format(total_rollout_prob),
              " |  Number of moves:  " if number_of_moves < 10 else " |  Number of moves: ", number_of_moves,
              " |  New buffer data:  " if len(buffer) - old_buffer_size < 10 else " |  New buffer data: ",
              len(buffer) - old_buffer_size,
              " |  Buffer dict size: ", len(buffer))

        actor.decrease_epsilon()
        rollout_prob = rollout_prob * config["rollout_prob_decay_rate"]
        total_rollout_prob = config["min_rollout_prob"] + rollout_prob

    return evaluation_history, last_game_history, saved_actor_count


def train_network(actor, buffer, buffer_inputs, buffer_targets, config):
    batch_inputs = buffer_inputs
    batch_targets = buffer_targets

    for ii in range(len(buffer_inputs)):
        buffer_input = buffer_inputs[ii]
        buffer_key = "".join(str(elem) for elem in buffer_input)
        buffer[buffer_key] = [buffer_input, buffer_targets[ii]]

    keys = list(buffer.keys())

    if len(keys) < config["buffer_size"]:
        for key in keys:
            batch_inputs.append(buffer[key][0])
            batch_targets.append(buffer[key][1])

    else:
        while len(batch_inputs) < config["buffer_size"]:
            key = keys[randrange(0, len(keys))]
            batch_inputs.append(buffer[key][0])
            batch_targets.append(buffer[key][1])

    print("Training actor network | Buffer size:", len(batch_inputs))
    actor.train_model(batch_inputs, batch_targets, config["batch_size"], config["epochs"])


def initialize_actor(config, name=False):
    if name:
        return Actor(config["epsilon"], config["epsilon_decay_rate"], name=name)
    return Actor(config["epsilon"],
                 config["epsilon_decay_rate"],
                 input_dim=2 * (config["size"] ** 2 + 1),
                 hidden_layers=config["actor_hidden_layers"],
                 optimizer=config["actor_optimizer"],
                 activation=config["actor_activation"],
                 learning_rate=config["actor_learning_rate"],
                 l2_reg=config["actor_l2_reg"],
                 loss=config["actor_loss"])


def initialize_critic(config, name=False):
    return Critic(input_dim=2 * (config["size"] ** 2 + 1),
                  hidden_layers=config["critic_hidden_layers"],
                  optimizer=config["critic_optimizer"],
                  activation=config["critic_activation"],
                  learning_rate=config["critic_learning_rate"],
                  l2_reg=config["critic_l2_reg"],
                  loss=config["critic_loss"],
                  name=name)


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
