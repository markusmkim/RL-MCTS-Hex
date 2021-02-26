import numpy as np


class NimBoard:
    def __init__(self, stones, max_n, next_player):
        self.stones = stones
        self.max_n = max_n
        self.next_player = next_player


    def move(self, n):
        self.stones -= n
        self.next_player = 1 if self.next_player == 0 else 0


    def get_possible_moves(self):
        a = np.arange(1, min(self.max_n, self.stones) + 1)
        return a


    def is_game_over(self):
        return self.stones == 0
