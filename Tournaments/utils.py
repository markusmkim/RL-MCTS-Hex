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
            board_row = [old_state[j][i]] + board_row
        flat_list = flat_list + bit_row
        board.append(board_row)

    print("board", board)

    input_list = player + flat_list

    possible_moves = []
    for i in range(0, len(flat_list), 2):
        if flat_list[i] == 0 and flat_list[i + 1] == 0:
            possible_moves.append(i // 2)

    chains = generate_chains(board)

    return [np.array(input_list), board, possible_moves, chains, None]


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
    player_1_chain_top = []     # top left
    player_1_chain_bottom = []  # bottom right

    # player 2
    player_2_chain_top = []     # top right
    player_2_chain_bottom = []  # bottom left

    # For hver chain:
    #     Legge alle brikker som befinner seg på kanten til den chainen som hører til den kanten
    #     Disse brikkene utgjør "køen"
    #     For hver brikke i køen:
    #         Legg alle naboer av samma farge til chainen og til køen, og fjern brikken fra køen
    #     Når køen er tom er chainen ferdig (?)
    for row in range(len(board)):
        for col in range(len(board)):
            if row == 0 and board[row][col] == 1:
                player_1_chain_top.append((row, col))
            if row == 5 and board[row][col] == 1:
                player_1_chain_bottom.append((row, col))
            if col == 0 and board[row][col] == 2:
                player_2_chain_bottom.append((row, col))
            if row == 0 and board[row][col] == 2:
                player_2_chain_top.append((row, col))

    chains = [player_1_chain_top, player_1_chain_bottom, player_2_chain_top, player_2_chain_bottom]
    for i in range(len(chains)):
        chain = chains[i]
        player = 1 if i < 2 else 2
        queue = []
        for cell in chain:
            queue.append(cell)

        processed = []
        while len(queue) > 0:
            cell_in_focus = queue.pop()
            processed.append(cell_in_focus)
            neighbours = get_neighbours(board, cell_in_focus[0], cell_in_focus[1], player)
            for n in neighbours:
                if n not in queue and n not in processed:
                    queue.append(n)
                if n not in chain:
                    chain.append(n)

    return [
        player_1_chain_top,
        player_1_chain_bottom,
        player_2_chain_top,
        player_2_chain_bottom
    ]


def get_neighbours(board, row, col, player):
    """
    Finds all neighbours for a given cell.
    A neighbour is defined as another cell that is directly connected to this cell AND has been filled by
    the same player as this cell (cell has same color).
    :param row: row-wise index of cell
    :param col: col-wise index of cell
    :param player: player
    :return: all neighbours
    """
    neighbours = []
    if row < len(board) - 1 and board[row + 1][col] == player:
        neighbours.append((row + 1, col))

    if row > 0 and board[row - 1][col] == player:
        neighbours.append((row - 1, col))

    if col < len(board) - 1 and board[row][col + 1] == player:
        neighbours.append((row, col + 1))

    if col > 0 and board[row][col - 1] == player:
        neighbours.append((row, col - 1))

    if row < len(board) - 1 and col < len(board) - 1 and board[row + 1][col + 1] == player:
        neighbours.append((row + 1, col + 1))

    if row > 0 and col > 0 and board[row - 1][col - 1] == player:
        neighbours.append((row - 1, col - 1))

    return neighbours

