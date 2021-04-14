from random import randrange


def generate_training_target(visits_dict, total_visits, size):
    training_target = []
    for k in range(size):
        if k in visits_dict:
            training_target.append(visits_dict[k] / total_visits)
        else:
            training_target.append(0)
    return training_target


def train_network(actor, buffer, buffer_counts, buffer_inputs, buffer_targets, total_number_of_moves, config):
    batch_inputs = buffer_inputs
    batch_targets = buffer_targets

    for ii in range(len(buffer_inputs)):
        buffer_input = buffer_inputs[ii]
        buffer_key = "".join(str(int(elem)) for elem in buffer_input)
        buffer[buffer_key] = [buffer_input, buffer_targets[ii], total_number_of_moves]

        if buffer_key in buffer_counts:
            buffer_counts[buffer_key] = buffer_counts[buffer_key] + 1
        else:
            buffer_counts[buffer_key] = 1

    keys = list(buffer.keys())

    if len(keys) < config["train_size"]:
        for key in keys:
            batch_inputs.append(buffer[key][0])
            batch_targets.append(buffer[key][1])

    else:
        while len(batch_inputs) < config["train_size"]:
            key = keys[randrange(0, len(keys))]
            batch_inputs.append(buffer[key][0])
            batch_targets.append(buffer[key][1])

    print("Training actor network | Train size:", len(batch_inputs))
    actor.train_model(batch_inputs, batch_targets, config["batch_size"], config["epochs"])


def prune_buffer(buffer, total_number_moves, buffer_size):
    limit = total_number_moves - buffer_size

    if len(buffer) - buffer_size < 0:
        return

    keys_to_remove = []
    for key in buffer:
        if buffer[key][2] < limit:
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del buffer[key]
