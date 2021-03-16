import numpy as np
from math import sqrt
import networkx as nx
import matplotlib.pyplot as plt
import copy


def get_next_state(state, action):
    copyManager = HexManager(copy.deepcopy(state))
    copyManager.execute_action(action)
    return copyManager.get_state()


class HexManager:
    def __init__(self, *args):
        self.history = []

        # args = [player, size]
        if len(args) > 1:
            self.player = args[0]
            self.grid = np.zeros(2 * (args[1]**2))
            self.possible_actions = np.arange(args[1]**2)

        # args = 'state' = [player, grid, possible_actions]
        else:
            self.player = args[0][0]
            self.grid = args[0][1]
            self.possible_actions = args[0][2]


    def execute_action(self, action):
        if self.player == 0:
            self.grid[2 * action] = 1
            # self.grid[2 * action + 1] = 0
        else:
            # self.grid[2 * action] = 0
            self.grid[2 * action + 1] = 1
        self.possible_actions = np.delete(self.possible_actions, np.where(self.possible_actions == action))
        self.player = int(self.player == 0)

        # save grid for displaying whole game later
        self.history.append(self.generate_board())


    def is_game_over(self):
        return len(self.possible_actions) == 0


    def get_winner(self):

        if not self.is_game_over():
            return None

        # player 0 is black and has the north-west and south-east sides
        # player 1 is red and has the north-east and south-west sides
        board = self.generate_board()

        # from the assignment we know that ties are not possible,
        # which means that if player 0 has not won, then player 1 has won
        winner = 1

        # try to find a winning chain for black (player 0)
        # there are size possible starting cells for a black chain, if one exists
        # these starting cells are the size first in the board (north west)
        size = int(sqrt(len(self.grid) / 2))

        possible_chains = []
        for i in range(size):
            if board[0][i] == 0:
                possible_chains.append(i)

        for i in range(1, size):
            next_possible_chains = []
            for cell in possible_chains:
                if board[i][cell] == 0:
                    next_possible_chains.append(cell)
                if cell < size - 1:
                    if board[i][cell + 1] == 0:
                        next_possible_chains.append(cell + 1)
            possible_chains = next_possible_chains

        if len(possible_chains) > 0:
            winner = 0

        return winner


    def get_state(self):
        return copy.deepcopy([self.player, self.grid, self.possible_actions])

    # returns 2d array representing the board
    def generate_board(self):
        size = int(sqrt(len(self.grid) / 2))
        flat_board = np.zeros(size**2)
        for i in range(len(self.grid)):
            if i % 2 == 0:
                if self.grid[i] == 0:
                    flat_board[i // 2] = -1
            else:
                if self.grid[i] == 1:
                    flat_board[i // 2] = 1

        board = []
        index = 0
        for i in range(size):
            row = []
            for j in range(size):
                row.append(flat_board[index])
                index += 1
            board.append(row)

        return board


    def visualize_game(self):
        for board in self.history:
            visualize_board(board)


    def visualize_game_state(self):
        board = self.generate_board()
        visualize_board(board)

    # ---- Debug / hjelpe  -funksjoner under --- #
    def visualize_board(self, board):
        visualize_board(board)


    def print_winner(self, board):
        winner = 1
        size = int(sqrt(len(self.grid) / 2))

        possible_chains = []
        for i in range(size):
            if board[0][i] == 0:
                possible_chains.append(i)

        for i in range(1, size):
            next_possible_chains = []
            for cell in possible_chains:
                if board[i][cell] == 0:
                    next_possible_chains.append(cell)
                if cell < size - 1:
                    if board[i][cell + 1] == 0:
                        next_possible_chains.append(cell + 1)
            possible_chains = next_possible_chains

        if len(possible_chains) > 0:
            winner = 0

        print(winner)

        # Notes for get_winner()
        # below are the possible next indexes for each index (for a black chain)
        # 0 -> 4 , 5
        # 1 -> 5 , 6
        # 2 -> 6 , 7
        # 3 -> 7

        # 4 -> 8 , 9
        # 5 -> 9 , 10
        # 6 -> 10 , 11
        # 7 -> 11

        # 8 -> 12 , 13
        # 9 -> 13 , 14
        # 10 -> 14 , 15
        # 11 -> 15


def visualize_board(grid):
    G = nx.Graph()

    # player 0
    black_nodes = []

    # player 1
    red_nodes = []

    # empty cell
    empty_nodes = []

    positions = {}

    # Add nodes
    for i in range(len(grid)):
        for j in range(len(grid)):

            # Add node
            G.add_node((i, j))

            # Split filled/unfilled nodes into different lists to apply different colors
            if grid[i][j] == 0:
                black_nodes.append((i, j))
            elif grid[i][j] == 1:
                red_nodes.append((i, j))
            else:
                empty_nodes.append((i, j))

            # Add edges
            if i > 0:
                if j == 0 or j == len(grid) - 1:
                    G.add_edge((i - 1, j), (i, j), color='#c21a0e', weight=3)
                else:
                    G.add_edge((i - 1, j), (i, j), color='black', weight=1)
            if j > 0:
                if i == 0 or i == len(grid) - 1:
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
    positions['dummy_node_2'] = ((len(grid) * 2) - 1, 0)
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
