from random import randint, random


class Actor:

    def __init__(self, epsilon):
        self.epsilon = epsilon


    def find_best_action(self, state):
        if len(state[2]) == 0:
            return None

        # returns random action
        if random() < self.epsilon:
            return state[2][randint(0, len(state[2]) - 1)]

        return state[2][randint(0, len(state[2]) - 1)]
