from MCTS.tree import Tree
from SimWorld.hexManager import HexManager, get_next_state
from SimWorld.utils import visualize_game
from time import time
from RL.utils import train_networks, generate_training_target, prune_buffer
from Main.utils import initialize_actor, display_buffer_counts_stats, display_episode_stats, display_time_stats, evaluate_progression


def run_rl_algorithm(actor, critic, config, tournaments, actors=None):
    print("Training models...")

    buffer_inputs = []
    buffer_targets = []

    buffer = {}
    buffer_counts = {}
    total_number_of_moves = 0

    last_game_history = []
    evaluation_history = []
    rph = []  # rollout prob history

    best_evaluation = 0
    saved_actor_count = 0

    rollout_prob = config["rollout_prob"]
    total_rollout_prob = config["min_rollout_prob"] + rollout_prob

    """ Time-stuff """
    last_save_start_time = time()
    time_history = []

    rollout_actor = False
    if config["rollout_actor"]:
        rollout_actor = initialize_actor(config, config["rollout_actor"])

    first_evaluation = evaluate_progression(actor, saved_actor_count, tournaments, config["size"])
    evaluation_history.append(first_evaluation)
    rph.append(min(1, total_rollout_prob))
    saved_actor_count += 1

    for i in range(1, config["episodes"] + 1):
        starting_player = [1, 0] if i % 2 == 0 else [0, 1]
        game_manager = HexManager(starting_player, config["size"])

        if i == config["episodes"]:
            last_game_history.append(game_manager.get_state()[1])

        tree = Tree(game_manager.get_state(), actor, critic)
        if rollout_actor:
            if i < config["rollout_actor_episodes"]:
                tree = Tree(game_manager.get_state(), rollout_actor, critic)
        tree.root.number_of_visits = 1

        number_of_moves = 0
        simulations = config["mcts_starting_simulations"]

        if i % config["save_frequency"] == 0 or i == config["episodes"]:
            last_game_history = [game_manager.get_state()[1]]

        while not game_manager.is_game_over():
            visits_dict, total_visits, action = tree.mcts(
                time(),
                get_next_state,
                config["c"],
                total_rollout_prob)

            buffer_inputs.append(game_manager.get_state()[0])
            buffer_targets.append(generate_training_target(visits_dict, total_visits, config["size"] ** 2))

            game_manager.execute_action(action)

            if i % config["save_frequency"] == 0 or i == config["episodes"]:
                last_game_history.append(game_manager.get_state()[1])

            if number_of_moves > config["mcts_move_increase"]:
                if number_of_moves > config["mcts_move_decrease"]:
                    simulations -= config["mcts_decrease_constant"]
                else:
                    simulations += config["mcts_increase_constant"]
            number_of_moves += 1

        old_buffer_size = len(buffer)

        train_networks(actor,
                       critic,
                       buffer,
                       buffer_counts,
                       buffer_inputs,
                       buffer_targets,
                       game_manager.get_winner(),
                       total_number_of_moves,
                       config,
                       i,
                       actors=actors)

        buffer_inputs = []
        buffer_targets = []

        if i % config["save_frequency"] == 0:
            print("Saving network")

            """ Time-stuff """
            if i > 0:
                time_spent_on_save = time() - last_save_start_time
                time_history.append(time_spent_on_save)
                display_time_stats(time_spent_on_save, time_history)

            evaluation = evaluate_progression(actor, saved_actor_count, tournaments, config["size"])
            evaluation_history.append(evaluation)
            rph.append(min(1, total_rollout_prob))
            saved_actor_count += 1

            if evaluation > best_evaluation:
                best_evaluation = evaluation
                actor.save_model("best_model_last_run")
                print("Best evaluation so far this run!")
            print("\n")

            prune_buffer(buffer, total_number_of_moves, config["buffer_size"])

            last_save_start_time = time()

        if config["visualize_game_on_every_save"] and i % config["save_frequency"] == 0:
            visualize_game(last_game_history)

        display_episode_stats(i,
                              starting_player,
                              game_manager.get_winner(),
                              actor.epsilon,
                              total_rollout_prob,
                              number_of_moves,
                              len(buffer),
                              old_buffer_size)

        actor.decrease_epsilon()
        rollout_prob = rollout_prob * config["rollout_prob_decay_rate"]
        total_rollout_prob = config["min_rollout_prob"] + rollout_prob
        total_number_of_moves += number_of_moves

    display_buffer_counts_stats(buffer_counts)
    return evaluation_history, last_game_history, saved_actor_count, rph
