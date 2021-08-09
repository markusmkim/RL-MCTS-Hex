from MCTS.node import Node
from time import time


class Tree:
    def __init__(self, root_state, actor, critic):
        self.root = Node(None, root_state)
        self.actor = actor
        self.critic = critic


    def mcts(self, start_time, get_next_state, c, rollout_prob):
        """
        Runs Monte Carlo Tree Search from the current root node.
        When the search has terminated, the best child of the root is selected as the new root, and the branches of the
        tree that are now unreachable are pruned.
        Returns the number of visits to each child node, the total number of visits, and the action that leads to the
        best (the most visited) child.
        """
        if self.root.children is None:
            self.root.expand(get_next_state)
        node = self.root
        while time() - start_time < 1:                          # run as many simulations as possible within 1 second
            while node.children and len(node.children) > 0:                 # traverse tree to find a leaf node
                node = node.best_child(c)
            if node.number_of_visits == 1:                                  # if leaf node is visited before
                node.expand(get_next_state)                                     # expand node
                if len(node.children) > 0:
                    node = node.children[0]
            value = node.rollout(self.actor, self.critic, rollout_prob)     # do rollout from leaf node
            while node.parent is not None:                                  # back-propagate values
                node = node.parent
                node.value += value
                node.number_of_visits += 1

        visits_dict, total_visits, best_child, best_action = self.root.children_visits()

        self.root = best_child
        self.root.parent = None

        return visits_dict, total_visits, best_action
