from random import randrange


def generate_training_target(visits_dict, total_visits, size):
    training_target = []
    for k in range(size):
        if k in visits_dict:
            training_target.append(visits_dict[k] / total_visits)
        else:
            training_target.append(0)
    return training_target


def train_networks(actor, critic, buffer, buffer_counts, buffer_inputs, buffer_targets, winner, n_moves, config, i):
    batch_inputs = buffer_inputs
    batch_targets = buffer_targets
    critic_target = [1, 0] if winner == 1 else [0, 1]
    critic_targets = [critic_target for _ in range(len(batch_inputs))]

    for ii in range(len(buffer_inputs)):
        buffer_input = buffer_inputs[ii]
        buffer_key = "".join(str(int(elem)) for elem in buffer_input)
        buffer[buffer_key] = [buffer_input, buffer_targets[ii], critic_target, n_moves]

        if buffer_key in buffer_counts:
            buffer_counts[buffer_key] = buffer_counts[buffer_key] + 1
        else:
            buffer_counts[buffer_key] = 1

    keys = list(buffer.keys())

    if i % 500 == 0:
        if len(keys) < config["train_size"]:
            for key in keys:
                batch_inputs.append(buffer[key][0])
                batch_targets.append(buffer[key][1])
                critic_targets.append(buffer[key][2])

        else:
            while len(batch_inputs) < config["train_size"]:
                key = keys[randrange(0, len(keys))]
                batch_inputs.append(buffer[key][0])
                batch_targets.append(buffer[key][1])
                critic_targets.append(buffer[key][2])

        print("Training networks | Train size:", len(batch_inputs))
        actor.train_model(batch_inputs, batch_targets, config["batch_size"], config["epochs"])
        if critic and config["train_critic"]:
            critic.train_model(batch_inputs, critic_targets, config["batch_size"], config["epochs"])


def prune_buffer(buffer, total_number_moves, buffer_size):
    limit = total_number_moves - buffer_size

    if len(buffer) - buffer_size < 0:
        return

    keys_to_remove = []
    for key in buffer:
        if buffer[key][3] < limit:
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del buffer[key]

