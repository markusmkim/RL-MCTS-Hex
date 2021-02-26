from MCTS.node import Node
from Agent.actor import Actor


class Tree:
    def __init__(self, initial_state):
        self.root = Node(None, initial_state)

    # kanskje gjøre Tree class sånn her, så ikke jeg glemmer det:

    def run_search(self):
        # use tree policy to traverse down to a leaf node
        leaf_node = 'some_node'
        # get_leaf_node state and do rollout
        self.rollout(leaf_node.state)


    def rollout(self, state):
        actor = Actor()
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