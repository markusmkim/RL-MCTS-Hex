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

            """
            Chains to ease the task of checking for a potential winner.
            Each player has to chains, one from the "top" of the board and one for the "bottom".
            For a particular player: 
            Each cell connected to the "top" will reside in the top chain, and vice versa. When a cell is in both
            chains, the player has won.
            """
            self.player_1_chain_top = []
            self.player_1_chain_bottom = []
            self.player_2_chain_top = []
            self.player_2_chain_bottom = []

            self.winner = None

        # args = 'state' = [input, board, possible_actions, chains, winner]
        else:
            self.player = args[0][0][:2]
            self.grid = args[0][0][2:]
            self.board = args[0][1]
            self.possible_actions = args[0][2]
            self.player_1_chain_top = args[0][3][0]
            self.player_1_chain_bottom = args[0][3][1]
            self.player_2_chain_top = args[0][3][2]
            self.player_2_chain_bottom = args[0][3][3]
            self.winner = args[0][4]


    def handleChains(self, row, col, player):
        """
        Manages and updates chains:

        - Checks if cell is in any of the chain's starting or stopping row or columns
          - If yes, cell will be added to corresponding chain
        - Checks for any neighbour cell if neighbour is in any of the two chains.
          - If yes, cell will be added to corresponding chain.

        - If cell is connected to both chains of respective player, game over and player has won.
        - If cell is added to one chain exactly, this function will be recursively called on all neighbours.

        :param row: row-wise index of cell
        :param col:  col-wise index of cell
        :param player: player to fill cell
        :return: name of winning player (1 or 2) if any, else 0
        """
        if player == 1:
            chain_top = self.player_1_chain_top
            chain_bottom = self.player_1_chain_bottom
        else:
            chain_top = self.player_2_chain_top
            chain_bottom = self.player_2_chain_bottom

        top, bottom = False, False
        neighbours = self.get_neighbours(row, col, player)  # neighbour = (row, col)

        if (player == 1 and row == 0) or (player == 2 and col == len(self.board) - 1):
            chain_top.append((row, col))
            for neighbour in neighbours:
                if neighbour in chain_bottom:
                    return player
                if neighbour not in chain_top:
                    self.handleChains(neighbour[0], neighbour[1], player)

        elif (player == 1 and row == len(self.board) - 1) or (player == 2 and col == 0):
            chain_bottom.append((row, col))
            for neighbour in neighbours:
                if neighbour in chain_top:
                    return player
                if neighbour not in chain_bottom:
                    self.handleChains(neighbour[0], neighbour[1], player)

        else:
            for neighbour in neighbours:
                if neighbour in chain_top and (row, col) not in chain_top:
                    chain_top.append((row, col))
                    top = True
                if neighbour in chain_bottom and (row, col) not in chain_bottom:
                    chain_bottom.append((row, col))
                    bottom = True

        if top and bottom:
            return player

        if top or bottom:
            for neighbour in neighbours:
                if neighbour not in chain_top and neighbour not in chain_bottom:
                    self.handleChains(neighbour[0], neighbour[1], player)

        return 0


    def get_neighbours(self, row, col, player):
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
        if row < len(self.board) - 1 and self.board[row + 1][col] == player:
            neighbours.append((row + 1, col))

        if row > 0 and self.board[row - 1][col] == player:
            neighbours.append((row - 1, col))

        if col < len(self.board) - 1 and self.board[row][col + 1] == player:
            neighbours.append((row, col + 1))

        if col > 0 and self.board[row][col - 1] == player:
            neighbours.append((row, col - 1))

        if row < len(self.board) - 1 and col < len(self.board) - 1 and self.board[row + 1][col + 1] == player:
            neighbours.append((row + 1, col + 1))

        if row > 0 and col > 0 and self.board[row - 1][col - 1] == player:
            neighbours.append((row - 1, col - 1))

        return neighbours


    def execute_action(self, action):
        row = action // len(self.board)
        col = action % len(self.board)

        self.possible_actions = np.delete(self.possible_actions, np.where(self.possible_actions == action))
        self.player = [int(self.player[0] == 0), int(self.player[1] == 0)]

        if self.player[0] == 0:
            self.grid[2 * action] = 1
            self.board[row][col] = 1
            winner = self.handleChains(row, col, 1)

        else:
            self.grid[2 * action + 1] = 1
            self.board[row][col] = 2
            winner = self.handleChains(row, col, 2)

        if winner != 0:
            self.winner = winner

    # state = [input, board, possible_moves] --> input = flat list of player + grid
    def get_state(self):
        chains = [
            self.player_1_chain_top,
            self.player_1_chain_bottom,
            self.player_2_chain_top,
            self.player_2_chain_bottom
        ]
        return copy.deepcopy([np.concatenate((self.player, self.grid)),
                              self.board,
                              self.possible_actions,
                              chains,
                              self.winner])


    def is_game_over(self):
        return self.get_winner() is not None


    def get_winner(self):
        return self.winner

    # player 1 = (1, 0) = black --> has the north-west and south-east sides
    # player 2 = (0, 1) = red   --> has the north-east and south-west sides
    def get_winner_old(self):

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
            return 1

        # try to find a winning chain for red (player 2)
        possible_chains = []
        for i in range(len(self.board)):
            if self.board[i][0] == 2:
                possible_chains.append(i)

        for i in range(1, len(self.board)):
            next_possible_chains = []
            for cell in possible_chains:
                if self.board[cell][i] == 2:
                    next_possible_chains.append(cell)
                if cell < len(self.board) - 1:
                    if self.board[cell + 1][i] == 2:
                        next_possible_chains.append(cell + 1)
            possible_chains = next_possible_chains

        if len(possible_chains) > 0:
            return 2

        return 0


    def visualize_game_state(self):
        visualize_board(self.board)


    def printChains(self):
        print("Black top: ", self.player_1_chain_top)
        print("Black bot: ", self.player_1_chain_bottom)
        print("Red top:   ", self.player_2_chain_top)
        print("Red bot:   ", self.player_2_chain_bottom)


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
