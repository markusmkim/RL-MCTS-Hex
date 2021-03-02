from SimWorld.nimManager import get_next_state
from SimWorld.nimManager import NimManager
from Agent.actor import Actor


class Node:
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        self.value = 0
        self.children = []


    def expand(self):
        if self.state[3] is None:
            self.children = None
            return None
        for action in self.state[3]:
            next_state = get_next_state(self.state.copy(), action)
            child = Node(self, next_state)
            self.children.append(child)
        return self.children


    def rollout(self):
        simulationManager = NimManager(self.state[0], self.state[1], self.state[2])
        simulationActor = Actor(0.1)
        node = self
        while not simulationManager.is_game_over():
            simulationAction = simulationActor.find_best_action(simulationManager.get_state())
            simulationManager.execute_action(simulationAction)
            child = Node(self, simulationManager.get_state())
            node.children.append(child)
            node = child
        self.value = 1 if simulationManager.get_state()[2] == 1 else -1
        return self.value
