from Tournaments.OHT.oht_node import Node
from time import time


class Tree:
    def __init__(self, root_state, actor):
        self.root = Node(None, root_state)
        self.actor = actor


    def mcts(self, start_time, get_next_state, c):
        if self.root.children is None:
            self.root.expand(get_next_state)
        node = self.root
        sim_count = 0
        while time() - start_time < 0.4:
            while node.children and len(node.children) > 0:
                node = node.best_child(c)
            if node.number_of_visits == 1:
                node.expand(get_next_state)
                if len(node.children) > 0:
                    node = node.children[0]
            value = node.rollout(self.actor)
            while node.parent is not None:
                node = node.parent
                node.value += value
                node.number_of_visits += 1
            sim_count += 1

        print("Number of simulations for this move:", sim_count)

        visits_dict, total_visits, best_child, best_action = self.root.children_visits()

        self.root = best_child
        self.root.parent = None

        return visits_dict, total_visits, best_action
