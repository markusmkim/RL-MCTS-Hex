import numpy as np
from copy import deepcopy
from SimWorld.utils import visualize_board


def get_next_state(state, action):
    copyManager = HexManager(deepcopy(state))
    copyManager.execute_action(action)
    return copyManager.get_state()


class HexManager:
    def __init__(self, *args):

        # args = [player, size]
        if len(args) > 1:
            self.player = args[0]
            self.grid = np.zeros(2 * (args[1] ** 2))
            self.board = np.zeros((args[1], args[1]))  # empty = 0, first/black player = 1, second/red player = 2
            self.possible_actions = np.arange(args[1] ** 2)

            """
            Chains to ease the task of checking for a potential winner.
            Each player has to chains, one from the "top" of the board and one for the "bottom".
            For a particular player: 
            Each cell connected to the "top" will reside in the top chain, and vice versa. When a cell is in both
            chains, the player has won.
            """
            self.top_right_chain = []
            self.bottom_left_chain = []
            self.top_left_chain = []
            self.bottom_right_chain = []

            self.winner = None

        # args = 'state' = [input, board, possible_actions, chains, winner]
        else:
            self.player = args[0][0][:2]
            self.grid = args[0][0][2:]
            self.board = args[0][1]
            self.possible_actions = args[0][2]
            self.top_right_chain = args[0][3][0]
            self.bottom_left_chain = args[0][3][1]
            self.top_left_chain = args[0][3][2]
            self.bottom_right_chain = args[0][3][3]
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
            chain_top = self.top_right_chain
            chain_bottom = self.bottom_left_chain
        else:
            chain_top = self.top_left_chain
            chain_bottom = self.bottom_right_chain

        top, bottom = False, False
        neighbours = self.get_neighbours(row, col, player)  # neighbour = (row, col)

        if (player == 2 and row == 0) or (player == 1 and col == len(self.board) - 1):
            chain_top.append((row, col))
            for neighbour in neighbours:
                if neighbour in chain_bottom:
                    return player
                if neighbour not in chain_top:
                    self.handleChains(neighbour[0], neighbour[1], player)

        elif (player == 2 and row == len(self.board) - 1) or (player == 1 and col == 0):
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

    # state = [input, board, possible_moves, chains, winner] --> input = flat list of player + grid
    def get_state(self):
        chains = [
            self.top_right_chain,
            self.bottom_left_chain,
            self.top_left_chain,
            self.bottom_right_chain
        ]
        return deepcopy([np.concatenate((self.player, self.grid)),
                         self.board,
                         self.possible_actions,
                         chains,
                         self.winner])


    def is_game_over(self):
        return self.get_winner() is not None


    def get_winner(self):
        return self.winner


    def visualize_game_state(self):
        visualize_board(self.board)


    def printChains(self):
        print("Black top: ", self.top_right_chain)
        print("Black bot: ", self.bottom_left_chain)
        print("Red top:   ", self.top_left_chain)
        print("Red bot:   ", self.bottom_right_chain)
