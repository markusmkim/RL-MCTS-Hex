from MCTS.node import Node
# from Agent.actor import Actor


class Tree:
    def __init__(self, root_state):
        self.root = Node(None, root_state)

    # returns number of nodes in the tree
    def generate_tree(self):
        queue = self.root.expand()
        count = len(queue)
        print("Root!")
        while len(queue) > 0:
            node = queue.pop(0)
            children = node.expand()
            if children:
                queue += children
                count += len(children)
            print("Expansion!", count)
        return count

    """
    def run_search(self):
        # use tree policy to traverse down to a leaf node
        leaf_node = 'some_node'
        # get_leaf_node state and do rollout
        self.rollout(leaf_node.state)
    """
