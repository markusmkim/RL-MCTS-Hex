from SimWorld.hexManager import HexManager
from SimWorld.hexManager import get_next_state
from MCTS.tree import Tree
from Agent.actor import Actor
from config import config
from tournament import Tournament


def generate_training_target(visits_dict, total_visits, size):
    training_target = []
    for k in range(size):
        if k in visits_dict:
            training_target.append(visits_dict[k] / total_visits)
        else:
            training_target.append(0)
    return training_target


actor = Actor(2 * (config["size"]**2 + 1), config["hidden_layers"], config["learning_rate"], config["epsilon"], config["epsilon_decay_rate"])

saved_actor_count = 0


print("Welcome to a game of Hex!")


for i in range(config["episodes"] + 1):
    game_history = []

    game_manager = HexManager([1, 0], 4)
    game_history.append(game_manager.get_state()[1])

    tree = Tree(game_manager.get_state(), actor)
    tree.root.number_of_visits = 1

    buffer_inputs = []
    buffer_targets = []

    while not game_manager.is_game_over():
        visits_dict, total_visits, action = tree.mcts(config["mcts_simulations"], get_next_state)

        buffer_inputs.append(game_manager.get_state()[0])
        buffer_targets.append(generate_training_target(visits_dict, total_visits, config["size"]**2))

        game_manager.execute_action(action)

        game_history.append(game_manager.get_state()[1])

    if i % config["save_frequency"] == 0:
        print('hei')
        actor.train_model(buffer_inputs, buffer_targets, count=saved_actor_count)
        saved_actor_count += 1
    else:
        actor.train_model(buffer_inputs, buffer_targets)

    print("Episode:", i, " |  Winner:", game_manager.get_winner(), " |  Epsilon: ", actor.epsilon)
    actor.decrease_epsilon()


tournament = Tournament(config)
tournament.run_tournament()





"""
game_manager = HexManager(0, 3)
tree = Tree(game_manager.get_state())
tree.root.number_of_visits = 1

black_1 = [[0, 1, 0], [0, 1, 1], [0, 1, 0]]
black_2 = [[1, 0, 1], [1, 1, 0], [0, 1, 0]]
black_3 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

red_1 = [[0, 0, 1], [0, 0, 0], [1, 1, 1]]
red_2 = [[1, 1, 0], [0, 0, 1], [0, 1, 0]]
red_3 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

bingo = [[1, 1, 1], [0, 0, 1], [1, 1, 1]]

game_manager.visualize_board(black_1)
game_manager.print_winner(black_1)
game_manager.print_winner(black_2)
game_manager.print_winner(black_3)

game_manager.print_winner(red_1)
game_manager.print_winner(red_2)
game_manager.print_winner(red_3)
"""

