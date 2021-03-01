from random import randint, random


class Actor:

    def __init__(self, epsilon):
        self.epsilon = epsilon


    def find_best_action(self, state):
        if state[0] == 0:
            return None

        # returns random action
        if random() < self.epsilon:
            return state[3][randint(0, len(state[3]) - 1)]

        # this game is possible to win in one move
        if state[0] in state[3]:
            return state[0]

        return state[3][randint(0, len(state[3]) - 1)]
