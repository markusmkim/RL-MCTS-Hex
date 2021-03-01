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


    def rollout(self, state):
        actor = Actor(0)
        game_state_manager = 'some SimWorld main class'
        game_state_manager.set_initial_state(state)
        while not game_state_manager.is_game_over():
            possible_moves = game_state_manager.get_possible_moves(state)
            move = actor.find_next_move(possible_moves)
            next_state = game_state_manager.make_move()
            state = next_state

        # find reward
        reward = 'some reward'
        return reward
    """
