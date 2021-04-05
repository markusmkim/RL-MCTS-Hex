from math import sqrt
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def print_winner(board):
    possible_chains = []
    for i in range(len(board)):
        if board[0][i] == 1:
            possible_chains.append(i)

    for i in range(1, len(board)):
        next_possible_chains = []
        for cell in possible_chains:
            if board[i][cell] == 1:
                next_possible_chains.append(cell)
            if cell < len(board) - 1:
                if board[i][cell + 1] == 1:
                    next_possible_chains.append(cell + 1)
        possible_chains = next_possible_chains

    if len(possible_chains) > 0:
        return 1

    # try to find a winning chain for red (player 2)
    possible_chains = []
    for i in range(len(board)):
        if board[i][0] == 2:
            possible_chains.append(i)

    for i in range(1, len(board)):
        next_possible_chains = []
        for cell in possible_chains:
            if board[cell][i] == 2:
                next_possible_chains.append(cell)
            if cell < len(board) - 1:
                if board[cell + 1][i] == 2:
                    next_possible_chains.append(cell + 1)
        possible_chains = next_possible_chains

    if len(possible_chains) > 0:
        return 2

    return 0


def visualize_board(board):
    G = nx.Graph()

    # player 0
    black_nodes = []

    # player 1
    red_nodes = []

    # empty cell
    empty_nodes = []

    positions = {}

    # Add nodes
    for i in range(len(board)):
        for j in range(len(board)):

            # Add node
            G.add_node((i, j))

            # Split filled/unfilled nodes into different lists to apply different colors
            if board[i][j] == 1:
                black_nodes.append((i, j))
            elif board[i][j] == 2:
                red_nodes.append((i, j))
            else:
                empty_nodes.append((i, j))

            # Add edges
            if i > 0:
                if j == 0 or j == len(board) - 1:
                    G.add_edge((i - 1, j), (i, j), color='#c21a0e', weight=3)
                else:
                    G.add_edge((i - 1, j), (i, j), color='black', weight=1)
            if j > 0:
                if i == 0 or i == len(board) - 1:
                    G.add_edge((i, j - 1), (i, j), color='black', weight=3)
                else:
                    G.add_edge((i, j - 1), (i, j), color='black', weight=1)
            if i > 0 and j > 0:
                G.add_edge((i - 1, j - 1), (i, j), color='black', weight=1)

            # Add positions
            positions[(i, j)] = (((i + j) * 0.8), j - i)  # Works like a coordinate system

    # Add dummy nodes for visual scaling
    dummy_nodes = ['dummy_node_1', 'dummy_node_2']
    G.add_nodes_from(dummy_nodes)
    positions['dummy_node_1'] = (-1, 0)
    positions['dummy_node_2'] = ((len(board) * 2) - 1, 0)
    nx.draw_networkx_nodes(G, positions, nodelist=dummy_nodes, node_color='w')  # Dummy nodes are white/invisible

    # Get edge colors and weights
    edge_colors = nx.get_edge_attributes(G, 'color').values()
    edge_weights = nx.get_edge_attributes(G, 'weight').values()

    # Draw network
    nx.draw_networkx_nodes(G, positions, nodelist=black_nodes, node_color='#2e3330', edgecolors="black")
    nx.draw_networkx_nodes(G, positions, nodelist=red_nodes, node_color='#e03428', edgecolors="black")
    nx.draw_networkx_nodes(G, positions, nodelist=empty_nodes, node_color='w', edgecolors="black")
    nx.draw_networkx_edges(G, positions, edge_color=edge_colors, width=list(edge_weights))
    plt.show()


def visualize_game(history):
    for board in history:
        visualize_board(board)


def generate_board(grid):
    size = int(sqrt(len(grid) / 2))
    flat_board = np.zeros(size**2)
    for i in range(len(grid)):
        if i % 2 == 0:
            if grid[i] == 1:
                flat_board[i // 2] = 1
        else:
            if grid[i] == 1:
                flat_board[i // 2] = 2
    board = []
    index = 0
    for i in range(size):
        row = []
        for j in range(size):
            row.append(flat_board[index])
            index += 1
        board.append(row)

    return board
