from SimWorld.hexManager import HexManager
from SimWorld.hexManager import get_next_state, print_winner, visualize_board, visualize_game
from MCTS.tree import Tree
from Agent.actor import Actor
from config import config
from tournament import Tournament


game_manager = HexManager([1, 0], 4)
print(game_manager.get_state())
game_manager.visualize_game_state()

game_manager.execute_action(5)
print(game_manager.get_state())
game_manager.visualize_game_state()


game_manager.execute_action(10)
print(game_manager.get_state())
game_manager.visualize_game_state()



