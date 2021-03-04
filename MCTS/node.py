from math import sqrt, log
from SimWorld.hexManager import HexManager
from Agent.actor import Actor
import copy


class Node:
    def __init__(self, parent, state):
        self.parent = parent

        # state[0] = player, state[1] = grid, state[2] = possible_actions
        self.state = state

        self.value = 0
        self.number_of_visits = 0
        self.children = None


    def expand(self, get_next_state):
        self.children = []
        if len(self.state[2]) == 0:  # no legal moves
            return None
        for action in self.state[2]:
            next_state = get_next_state(self.state, action)
            child = Node(self, next_state)
            self.children.append(child)
        return self.children


    def rollout(self):
        # print("Rollout starts. Number of possible moves:", len(self.state[2]))
        simulation_manager = copy.deepcopy(HexManager(self.state))
        simulation_actor = Actor(0.1)
        while not simulation_manager.is_game_over():
            simulation_action = simulation_actor.find_best_action(simulation_manager.get_state())
            simulation_manager.execute_action(simulation_action)
            # print("Rollout! Game over:", simulation_manager.is_game_over())

        self.value = 1 if simulation_manager.get_winner() == 0 else -1
        self.number_of_visits += 1
        # print("Rollout done!")
        return self.value


    def best_child(self, c):
        if len(self.children) > 0:
            if self.state[0] == 0:
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


    def children_visits(self):
        visits_dict = {}
        total_visits = 0
        best_child_index = 0
        best_child = self.children[0]
        for index, child in enumerate(self.children):
            child_visits = child.number_of_visits
            visits_dict[self.state[2][index]] = child_visits
            total_visits += child_visits
            if child.number_of_visits > best_child.number_of_visits:
                best_child = child
                best_child_index = index

        return visits_dict, total_visits, best_child, self.state[2][best_child_index]



