from SimWorld.hexManager import HexManager
from SimWorld.hexManager import get_next_state, print_winner, visualize_board, visualize_game
from MCTS.tree import Tree
from Agent.actor import Actor
from config import config
from tournament import Tournament
from random import randint
from time import sleep
import copy

game_manager = HexManager([1, 0], 6)

for i in range(50):
    possible_actions = game_manager.get_state()[2]
    if len(possible_actions) == 0:
        break
    old_board = copy.deepcopy(game_manager.board)
    winner = game_manager.execute_action(possible_actions[randint(0, len(possible_actions) - 1)])
    print(winner)
    # print(game_manager.get_state())
    # game_manager.printChains()
    # game_manager.visualize_game_state()
    if winner > 0:                              # når en har vunnet
        visualize_board(old_board)              # print siste state før seier
        sleep(1)
        game_manager.visualize_game_state()     # print state hvor en har seiret
        break
    # sleep(1)



"""
print("")

print(game_manager.execute_action(9))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()

print("")

print(game_manager.execute_action(3))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()

print("")

print(game_manager.execute_action(6))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()


print("")

print(game_manager.execute_action(4))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()


print("")

print(game_manager.execute_action(1))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()


print("")

print(game_manager.execute_action(15))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()

print("")

print(game_manager.execute_action(13))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()

print("")

print(game_manager.execute_action(0))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()

print("")

print(game_manager.execute_action(8))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()
"""