

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

    new_state = player + flat_list

    return new_state


def convert_action(action, size):
    row = size - 1 - (action % size)
    column = action // size
    return row, column


