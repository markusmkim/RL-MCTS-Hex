import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import copy


class HexManager:
    def __init__(self, *args):

        # args = [player, size]
        if len(args) > 1:
            self.player = args[0]
            self.grid = np.zeros(2 * (args[1]**2))
            self.board = np.zeros((args[1], args[1]))  # empty = 0, first/black player = 1, second/red player = 2
            self.possible_actions = np.arange(args[1]**2)

        # args = 'state' = [input, board, possible_actions]
        else:
            self.player = args[0][0][:2]
            self.grid = args[0][0][2:]
            self.board = args[0][1]
            self.possible_actions = args[0][2]


    def execute_action(self, action):
        row = action // len(self.board)
        col = action % len(self.board)
        if self.player[0] == 1:
            self.grid[2 * action] = 1
            self.board[row][col] = 1
        else:
            self.grid[2 * action + 1] = 1
            self.board[row][col] = 2
        self.possible_actions = np.delete(self.possible_actions, np.where(self.possible_actions == action))
        self.player = [int(self.player[0] == 0), int(self.player[1] == 0)]

   # state = [input, board, possible_moves] --> input = flat list of player + grid
    def get_state(self):
        return copy.deepcopy([np.concatenate((self.player, self.grid)), self.board, self.possible_actions])


    def is_game_over(self):
        return len(self.possible_actions) == 0

    # player 1 = (1, 0) = black --> has the north-west and south-east sides
    # player 2 = (0, 1) = red   --> has the north-east and south-west sides
    def get_winner(self):

        if not self.is_game_over():
            return None

        winner = 2

        # try to find a winning chain for black (player 1)
        possible_chains = []
        for i in range(len(self.board)):
            if self.board[0][i] == 1:
                possible_chains.append(i)

        for i in range(1, len(self.board)):
            next_possible_chains = []
            for cell in possible_chains:
                if self.board[i][cell] == 1:
                    next_possible_chains.append(cell)
                if cell < len(self.board) - 1:
                    if self.board[i][cell + 1] == 1:
                        next_possible_chains.append(cell + 1)
            possible_chains = next_possible_chains

        if len(possible_chains) > 0:
            winner = 1

        return winner


    def visualize_game_state(self):
       visualize_board(self.board)


def get_next_state(state, action):
    copyManager = HexManager(copy.deepcopy(state))
    copyManager.execute_action(action)
    return copyManager.get_state()


def visualize_game(history):
    for board in history:
        visualize_board(board)


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


"""
# returns 2d array from 1d grid representing the board
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
"""
