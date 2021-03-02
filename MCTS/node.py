from SimWorld.nimManager import get_next_state
from SimWorld.nimManager import NimManager
from Agent.actor import Actor


class Node:
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        self.value = 0
        self.number_of_visits = 0
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

            # Vi skal vel ikke bygge treet når vi kjører rollout?
            # child = Node(self, simulationManager.get_state())
            # node.children.append(child)
            # node = child

        self.value = 1 if simulationManager.get_state()[2] == 1 else -1
        self.number_of_visits += 1
        return self.value

    # Må huske på at vi annenhver gang ønsker å maksimere og minimere score avhengig av spiller
    def best_child(self):
        if len(self.children) > 0:
            best_child = self.children[0]
            best_score = some_function(best_child)
            for child in self.children[1:]:
                if some_function(child) > best_score:
                    best_child = child
            return best_child
        return None

