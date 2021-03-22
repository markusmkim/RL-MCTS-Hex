from SimWorld.hexManager import HexManager
from SimWorld.hexManager import get_next_state, print_winner, visualize_board, visualize_game
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


actor = Actor(2 * (config["size"]**2 + 1),
              config["hidden_layers"],
              config["optimizer"],
              config["learning_rate"],
              config["epsilon"],
              config["epsilon_decay_rate"])

saved_actor_count = 0

print("Welcome to a game of Hex!")


for i in range(config["episodes"] + 1):
    game_history = []

    starting_player = [1, 0] if i % 2 == 0 else [0, 1]

    game_manager = HexManager(starting_player, config["size"])
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
    # visualize_game(game_history)
    actor.decrease_epsilon()


tournament = Tournament(config)
tournament.run_tournament()


"""
black_1 = [[2, 1, 2], [2, 1, 1], [2, 1, 2]]
black_2 = [[1, 2, 1], [1, 1, 2], [2, 1, 2]]
black_3 = [[2, 2, 2], [2, 2, 2], [2, 2, 2]]

red_1 = [[2, 2, 1], [2, 2, 2], [1, 1, 1]]
red_2 = [[1, 1, 2], [2, 2, 1], [2, 1, 2]]
red_3 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

bingo = [[2, 1, 1, 2], [1, 2, 1, 2], [1, 1, 1, 1], [2, 1, 1, 1]]

visualize_board(bingo)
print_winner(bingo)
#print_winner(black_2)
#print_winner(black_3)

#print_winner(red_1)
#print_winner(red_2)
#print_winner(red_3)
"""





