from MCTS.node import Node


class Tree:
    def __init__(self, root_state):
        self.root = Node(None, root_state)


    def mcts(self, number_of_simulations, actor, game_manager, get_next_state):
        if self.root.children is None:
            self.root.expand(get_next_state)
        node = self.root
        for i in range(number_of_simulations):
            while node.children and len(node.children) > 0:
                node = node.best_child(1)
            if node.number_of_visits == 1:
                node.expand(get_next_state)
                if len(node.children) > 0:
                    node = node.children[0]
            value = node.rollout(actor, game_manager)
            while node.parent is not None:
                node = node.parent
                node.value += value
                node.number_of_visits += 1

        visits_dict, total_visits, best_child, best_action = self.root.children_visits()

        self.root = best_child
        self.root.number_of_visits = 1

        return visits_dict, total_visits, best_action
