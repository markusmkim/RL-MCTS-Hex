from SimWorld.nimManager import get_next_state


class Node:
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
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
