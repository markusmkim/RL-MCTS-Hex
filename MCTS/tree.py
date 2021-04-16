from MCTS.node import Node


class Tree:
    def __init__(self, root_state, actor, critic):
        self.root = Node(None, root_state)
        self.actor = actor
        self.critic = critic


    def mcts(self, number_of_simulations, get_next_state, c, rollout_prob):
        if self.root.children is None:
            self.root.expand(get_next_state)
        node = self.root
        for i in range(number_of_simulations):
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
