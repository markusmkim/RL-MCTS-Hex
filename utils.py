
def generate_training_target(visits_dict, total_visits, size):
    training_target = []
    for k in range(size):
        if k in visits_dict:
            training_target.append(visits_dict[k] / total_visits)
        else:
            training_target.append(0)
    return training_target


def save_metadata(config, filepath, win_rate, time_spent):
    data = [f"{key}: {config[key]}" for key in config]
    file = open(filepath, "w")  # w = overwrite if already exists
    [file.write(line + "\n") for line in data]
    file.write("\nWin rate in OneVsAll: " + str(win_rate))
    file.write("\nTime spent: " + str(time_spent))
    file.close()


def read_metadata(filepath):
    numeric_keys = ["size",
                    "episodes",
                    "mcts_simulations",
                    "learning_rate",
                    "training_frequency",
                    "training_probability",
                    "epsilon",
                    "epsilon_decay_rate",
                    "TOPP-G",
                    "c"]
    data = {}
    file = open(filepath, "r")
    try:
        for line in file.readlines():
            if line == "":
                break
            config_line = line.split(": ")
            if len(config_line) == 2:
                key = config_line[0]
                value = config_line[1].rstrip()
                if key in numeric_keys:
                    value = float(value)

                if key == "save_frequency" and value != "None":
                    value = float(value)

                if key == "hidden_layers":
                    value = [int(layer) for layer in value[1:-1].split(", ")]

                data[key] = value
    finally:
        file.close()
    return data


def read_kings():
    path = "Agent/saved_networks/kings.txt"
    return read_royalty(path)


def read_queens():
    path = "Agent/saved_networks/queens.txt"
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
    path = "Agent/saved_networks/kings.txt"
    save_royalty(path, data)


def save_queens(data):
    """
    :param data: Dictionary of type {name: win_rate}
    """
    path = "Agent/saved_networks/queens.txt"
    save_royalty(path, data)


def save_royalty(filepath, data):
    file = open(filepath, "w")
    try:
        data = [f"{key}: {data[key]}" for key in data]
        [file.write(line + "\n") for line in data]
    finally:
        file.close()
