from SimWorld.nimManager import NimManager
from SimWorld.nimManager import get_next_state
from Agent.actor import Actor
from MCTS.tree import Tree

print("")
print("Welcome to a game of Nim!")
print("")

episodes = 100
count = 0
for i in range(episodes):
    print("Episode", i)

    game = NimManager(17, 5, 0)
    actor = Actor(0.2)
    player = 0
    tree = Tree(game.get_state().copy())
    tree.root.number_of_visits = 1
    while not game.is_game_over():
        # print("There are", game.get_state()[0], "stones left.")
        visits_dict, total_visits, action = tree.mcts(1200, Actor, NimManager, get_next_state)
        # print("Player", player, "removes", action, "stones.")
        game.execute_action(action)
        player = game.player
    count += game.get_winner()

print("")
print('Win rate:', (episodes - count) / episodes)
# print('Count', count)
