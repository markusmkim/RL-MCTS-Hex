from MCTS.node import Node
from time import time


class Tree:
    def __init__(self, root_state, actor, critic):
        self.root = Node(None, root_state)
        self.actor = actor
        self.critic = critic


    def mcts(self, time_limit, get_next_state, c, rollout_prob):
        if self.root.children is None:
            self.root.expand(get_next_state)
        node = self.root
        start_time = time()
        while time() - start_time < time_limit:
            while node.children and len(node.children) > 0:
                node = node.best_child(c)
            if node.number_of_visits == 1:
                node.expand(get_next_state)
                if len(node.children) > 0:
                    node = node.children[0]
            value = node.rollout(self.actor, self.critic, rollout_prob)
            while node.parent is not None:
                node = node.parent
                node.value += value
                node.number_of_visits += 1

        visits_dict, total_visits, best_child, best_action = self.root.children_visits()

        self.root = best_child
        self.root.parent = None

        return visits_dict, total_visits, best_action
