from SimWorld.nimManager import get_next_state
from SimWorld.nimManager import NimManager
from Agent.actor import Actor
from math import sqrt, log


class Node:
    def __init__(self, parent, state):
        self.parent = parent

        # state[0] = stones, state[1] = max_stones, state[2] = player, state[3] = possible_actions
        self.state = state

        self.value = 0
        self.number_of_visits = 0
        self.children = None


    def expand(self):
        if self.state[3] is None:
            self.children = []
            return None
        for action in self.state[3]:
            next_state = get_next_state(self.state.copy(), action)
            child = Node(self, next_state)
            self.children.append(child)
        return self.children


    def rollout(self):
        simulationManager = NimManager(self.state[0], self.state[1], self.state[2])
        simulationActor = Actor(0.1)

        while not simulationManager.is_game_over():
            simulationAction = simulationActor.find_best_action(simulationManager.get_state())
            simulationManager.execute_action(simulationAction)

        self.value = 1 if simulationManager.player_won == 1 else -1
        self.number_of_visits += 1
        return self.value


    def best_child(self, c):
        if len(self.children) > 0:
            if self.state[2] == 0:
                return self.argmax(c)
            return self.argmin(c)
        return None


    def argmax(self, c):
        best_child = self.children[0]
        best_score = self.evaluate_edge(c, best_child)
        for child in self.children[1:]:
            score = self.evaluate_edge(c, child)
            if score > best_score:
                best_child = child
                best_score = score
        return best_child


    def argmin(self, c):
        best_child = self.children[0]
        best_score = self.evaluate_edge(c, best_child)
        for child in self.children[1:]:
            score = self.evaluate_edge(c, child)
            if score < best_score:
                best_child = child
                best_score = score
        return best_child


    def evaluate_edge(self, c, child):
        # returns Q(s, a) + u(s, a)
        return child.value + c * sqrt(log(self.number_of_visits) / (1 + child.number_of_visits))
