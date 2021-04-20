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
    board = []

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
        bit_row = []
        board_row = []
        for j in range(size):  # row
            bit_representation = [0, 0]
            if old_state[j][i] == 1:
                bit_representation = [0, 1]
            elif old_state[j][i] == 2:
                bit_representation = [1, 0]
            bit_row = bit_representation + bit_row
            board_row = old_state[j][i] + board_row
        flat_list = flat_list + bit_row
        board = board + board_row

    input_list = player + flat_list

    possible_moves = []
    for i in range(0, len(flat_list), 2):
        if flat_list[i] == 0 and flat_list[i + 1] == 0:
            possible_moves.append(i // 2)

    chains = generate_chains(board)

    return [np.array(input_list), None, possible_moves, chains, None]


def convert_action(action, size):
    row = size - 1 - (action % size)
    column = action // size
    return row, column


def plot_stats(wins, episodes_list):
    plt.bar(episodes_list, wins, width=8)
    plt.xticks(episodes_list)
    plt.title("TOPP-Tournament")
    plt.show()


def generate_chains(board):

    # player 1
    north_east_chains = []
    south_west_chains = []

    # player 2
    north_west_chains = []
    south_east_chains = []

    # TODO: Calculate chains
    # For hver chain:
    #     Legge alle brikker som befinner seg på kanten til den chainen som hører til den kanten
    #     Disse brikkene utgjør "køen"
    #     For hver brikke i køen:
    #         Legg alle naboer av samma farge til chainen og til køen, og fjern brikken fra køen
    #     Når køen er tom er chainen ferdig (?)

    return [
        north_east_chains,
        south_west_chains,
        north_west_chains,
        south_east_chains
    ]
