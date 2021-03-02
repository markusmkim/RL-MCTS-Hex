from SimWorld.nimManager import NimManager
from Agent.actor import Actor
from MCTS.tree import Tree

game = NimManager(12, 3, 0)
actor = Actor(0.2)

player = 0

print("")
print("Welcome to a game of Nim!")
print("")

while not game.is_game_over():
    print("")
    print("There are", game.get_state()[0], "stones left.")
    tree = Tree(game.get_state().copy())
    print("The count of the tree is", tree.generate_tree())
    action = actor.find_best_action(game.get_state())
    print("Player", player, "removes", action, "stones.")
    game.execute_action(action)
    player = int(player == 0)

print("")
print('Winner:', int(player == 0))
