from Tournaments.OHT.oht_tree import Tree
from SimWorld.hexManager import get_next_state
from time import time
from random import randint
from RL.utils import generate_training_target


class OhtActor:

    def find_best_action_by_mcts(self, state):
        tree = Tree(state, self)
        tree.root.number_of_visits = 1
        v, _, action = tree.mcts(time(), get_next_state, 10)
        return action


    def find_best_action(self, state):
        if len(state[2]) == 0:
            print("INGEN MOVES")
        else:
            return state[2][randint(0, len(state[2]) - 1)]
