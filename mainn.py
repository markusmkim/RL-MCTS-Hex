from SimWorld.hexManager import HexManager
from SimWorld.hexManager import get_next_state
from MCTS.tree import Tree


print("")
print("Welcome to a game of Hex!")
print("")

episodes = 1

for i in range(episodes):
    print("Episode", i)

    game_manager = HexManager(0, 3)
    tree = Tree(game_manager.get_state())
    tree.root.number_of_visits = 1

    while not game_manager.is_game_over():
        game_manager.visualize_game()
        # print("States:")
        # print("Root state:", tree.root.state)
        # print("Game state:", game_manager.get_state())
        visits_dict, total_visits, action = tree.mcts(50, get_next_state)
        # print("Action:", action)
        game_manager.execute_action(action)
    game_manager.visualize_game()
