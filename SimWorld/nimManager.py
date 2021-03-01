import numpy as np


def get_next_state(state, action):
    copyManager = NimManager(state[0], state[1], state[2])
    copyManager.execute_action(action)
    return copyManager.get_state()


class NimManager:
    def __init__(self, stones, max_stones, first_player):
        self.stones = stones
        self.max_stones = max_stones
        self.player = first_player


    def execute_action(self, action):
        self.stones -= action
        self.player = int(self.player == 0)


    def is_game_over(self):
        return self.stones == 0


    def get_state(self):
        possible_actions = np.arange(1, min(self.max_stones, self.stones) + 1)
        if len(possible_actions) == 0:
            possible_actions = None
        return [self.stones, self.max_stones, self.player, possible_actions]
