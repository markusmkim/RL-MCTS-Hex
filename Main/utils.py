import matplotlib.pyplot as plt
import numpy as np
from Agent.actor import Actor
from Agent.critic import Critic


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


def display_buffer_counts_stats(buffer_counts):
    n_single_counts = 0
    total_count = 0
    counts = []

    for key in buffer_counts:
        count = buffer_counts[key]
        counts.append(count)
        total_count += count
        if count == 1:
            n_single_counts += 1

    n_single_counts_ratio = n_single_counts / len(buffer_counts)
    average = total_count / len(buffer_counts)

    print("Percentage of states visited only one time:", n_single_counts_ratio,
          " | Average number of visits to a state:", average)

    counts.sort()
    x_axis = np.arange(len(counts))
    plt.plot(x_axis, counts)
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    plt.show()


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


def read_elites():
    path = "Agent/saved_models/elites.txt"
    data = {}
    file = open(path, "r")
    try:
        for line in file.readlines():
            name_score = line.split(": ")
            if len(name_score) == 2:
                data[name_score[0]] = name_score[1].rstrip()
    finally:
        file.close()
    return data


def save_elites(data):
    path = "Agent/saved_models/elites.txt"
    file = open(path, "w")
    try:
        data = [f"{key}: {data[key]}" for key in data]
        [file.write(line + "\n") for line in data]
    finally:
        file.close()
