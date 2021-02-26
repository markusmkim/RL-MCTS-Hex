from MCTS.node import Node


class Tree:
    def __init__(self, initial_state):
        self.root = Node(None, initial_state)

