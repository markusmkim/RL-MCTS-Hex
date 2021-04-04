from SimWorld.hexManager import HexManager
from SimWorld.hexManager import get_next_state, print_winner, visualize_board, visualize_game
from MCTS.tree import Tree
from Agent.actor import Actor
from config import config
from tournaments import Tournaments
from random import randint
from time import sleep
import copy
from math import sqrt
import numpy as np

from OHT.BasicClientActor import BasicClientActor

basicClientActor = BasicClientActor()

state = [2, 0, 1, 1, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 1, 0]


def generate_board(grid):
    size = int(sqrt(len(grid) / 2))
    flat_board = np.zeros(size**2)
    for i in range(len(grid)):
        if i % 2 == 0:
            if grid[i] == 1:
                flat_board[i // 2] = 1
        else:
            if grid[i] == 1:
                flat_board[i // 2] = 2
    board = []
    index = 0
    for i in range(size):
        row = []
        for j in range(size):
            row.append(flat_board[index])
            index += 1
        board.append(row)

    return board


print(basicClientActor.handle_get_action(state, 4))


"""
game_manager = HexManager([1, 0], 4)

while not game_manager.is_game_over():
    possible_actions = game_manager.get_state()[2]
    if len(possible_actions) == 0:
        break
    old_board = copy.deepcopy(game_manager.board)
    game_manager.execute_action(possible_actions[randint(0, len(possible_actions) - 1)])

winner = game_manager.get_winner()
print(winner)
# print(game_manager.get_state())
# game_manager.printChains()
# game_manager.visualize_game_state()
if winner > 0:                              # når en har vunnet
    visualize_board(old_board)              # print siste state før seier
    sleep(1)
    game_manager.visualize_game_state()     # print state hvor en har seiret
"""



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