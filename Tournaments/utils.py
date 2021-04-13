import numpy as np
import matplotlib.pyplot as plt


def print_stats(stats, games, detailed_stats):
    print("")
    print("Stats:")
    print(stats)
    print("")
    print("Number of games:")
    print(games)
    print("")
    print("Detailed stats:")
    print(detailed_stats)
    print("")


def convert_state(oht_state, size):
    flat_list = []
    player = [1, 0]
    if oht_state[0] == 1:
        player = [0, 1]

    old_state = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(oht_state[1:][(i * size) + j])
        old_state.append(row)

    for i in range(size):  # column
        row = []
        for j in range(size):  # row
            bit_representation = [0, 0]
            if old_state[j][i] == 1:
                bit_representation = [0, 1]
            elif old_state[j][i] == 2:
                bit_representation = [1, 0]
            row = bit_representation + row
        flat_list = flat_list + row

    input_list = player + flat_list

    possible_moves = []
    for i in range(0, len(flat_list), 2):
        if flat_list[i] == 0 and flat_list[i + 1] == 0:
            possible_moves.append(i // 2)

    return [np.array(input_list), None, possible_moves]


def convert_action(action, size):
    row = size - 1 - (action % size)
    column = action // size
    return row, column


def plot_stats(wins, episodes_list):
    plt.bar(episodes_list, wins)
    plt.show()

