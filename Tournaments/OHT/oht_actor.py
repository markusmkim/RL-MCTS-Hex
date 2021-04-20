from Tournaments.OHT.oht_tree import Tree
from SimWorld.hexManager import get_next_state
from time import time
from random import randint


class OhtActor:

    def find_best_action_by_mcts(self, state):
        tree = Tree(state, self,)
        tree.root.number_of_visits = 1
        v, _, action = tree.mcts(time(), get_next_state, 3)
        # print(v)
        return action


    def find_best_action(self, state):
        return state[2][randint(0, len(state[2]) - 1)]
