

class Node:
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        # verdier

        self.children = []


    def expand(self, possible_moves, get_next_state):
        for move in possible_moves:
            next_state = get_next_state(move)
            child = Node(self, next_state)
            self.children.append(child)


    def rollout(self, actor):
        reward = actor.rollout()
