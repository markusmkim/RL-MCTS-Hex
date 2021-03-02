import numpy as np


def get_next_state(state, action):
    copyManager = HexManager(state)
    copyManager.execute_action(action)
    return copyManager.get_state()


class HexManager:
    def __init__(self, *args):
        if len(args) > 1:
            self.player = args[1]
            self.grid = np.zeros(2 * (args[0]**2))
            self.possible_actions = np.arange(args[0]**2)

        else:
            self.player = args[0][-1]
            self.grid = args[0][:-1]
            self.possible_actions = args[1]


    def execute_action(self, action):
        if self.player == 0:
            self.grid[2*action] = 1
        else:
            self.grid[2*action + 1] = 1
        self.possible_actions.remove(action)
        self.player = int(self.player == 0)


    def is_game_over(self):
        return 0


    def get_winner(self):
        return 0


    def get_state(self):
        return [self.grid.copy().append(self.player), self.possible_actions]


    def get_possible_actions(self):
        return self.possible_actions


