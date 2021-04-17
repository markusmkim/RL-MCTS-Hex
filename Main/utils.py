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


def evaluate_progression(actor, saved_actor_count, tournaments, size, final=False, plot_topp=False):
    actor.save_model("training", saved_actor_count)

    if saved_actor_count > 0:
        tournaments.run_topp_tournament(number_of_actors=None if final else saved_actor_count + 1, plot=plot_topp)

    if size == 6:
        evaluation = tournaments.evaluate_actor(actor, display=False)
    else:
        evaluation = tournaments.run_one_vs_all(actor, 9, display=False)

    time_expression = "Final" if final else "First" if saved_actor_count == 0 else "Intermediate"
    s = time_expression + " evaluation:"
    print(s, evaluation)
    return evaluation


def display_episode_stats(episode, starting_player, winner, epsilon, rollout_prob, n_moves, buff_size, old_buff_size):
    print("Episode:", episode,
          " |  Starting player: ", starting_player,
          " |  Winner: ", winner,
          " |  Epsilon: ", epsilon,
          " |  Rollout prob: ", "{:.3f}".format(rollout_prob),
          " |  Number of moves:  " if n_moves < 10 else " |  Number of moves: ", n_moves,
          " |  New buffer data:  " if buff_size - old_buff_size < 10 else " |  New buffer data: ",
          buff_size - old_buff_size,
          " |  Buffer dict size: ", buff_size)


def display_time_stats(time_spent_on_save, time_history):
    if len(time_history) > 1:
        time_spent_on_last_save = time_history[-2]
        ratio = time_spent_on_save / time_spent_on_last_save
        print("Time spent on current save:  ", time_spent_on_save)
        print("Time spent on previous save: ", time_spent_on_last_save)
        print("Ratio:", ratio)
        print("Time history:", time_history)
    else:
        print("Time spent on first save:", time_spent_on_save)


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
    plt.title("Buffer counts distribution")
    plt.show()


def plot_histories(histories, labels, frequency):
    x_axis = np.arange(len(histories[0])) * frequency
    for i in range(len(histories)):
        plt.plot(x_axis, histories[i], label=labels[i])
    plt.legend(fontsize="large")
    plt.title("History")
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
