from MCTS.node import Node
# from Agent.actor import Actor


class Tree:
    def __init__(self, root_state):
        self.root = Node(None, root_state)


    def mcts(self, number_of_simulations):
        if self.root.children is None:
            self.root.expand()
        node = self.root
        for i in range(number_of_simulations):
            while node.children and len(node.children) > 0:
                node = self.root.best_child(1)
            if node.number_of_visits == 1:
                node.expand()
                if len(node.children) > 0:
                    node = node.children[0]
            value = node.rollout()
            while node.parent is not None:
                node = node.parent
                node.value += value
                node.number_of_visits += 1

        best_child = self.root.best_child(0)
        child_index = self.root.children.index(best_child)
        action = self.root.state[3][child_index]
        self.root = best_child

        return action





    """
    def run_search(self):
        # use tree policy to traverse down to a leaf node
        leaf_node = 'some_node'
        # get_leaf_node state and do rollout
        self.rollout(leaf_node.state)
    """
