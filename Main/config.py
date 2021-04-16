config = {
    "name": "tungSize4",
    "train_from": False,
    "size": 4,

    "plot_evaluation_history": True,
    "visualize_last_game": False,
    "visualize_game_on_every_save": False,
    "run_interaction_game": False,

    "epsilon": 0.01,
    "epsilon_decay_rate": 1,
    "rollout_prob": 1000,
    "min_rollout_prob": 0.2,
    "rollout_prob_decay_rate": 0.995,

    "actor_hidden_layers": [64, 64],
    "actor_optimizer": 'adam',
    "actor_activation": 'relu',
    "actor_learning_rate": 0.005,
    "actor_loss": "mse",
    "actor_l2_reg": 0.0001,

    "rollout_actor":  False,
    "rollout_actor_episodes": 0,

    "use_critic": True,
    "critic_hidden_layers": [64, 64],
    "critic_optimizer": 'adam',
    "critic_activation": 'relu',
    "critic_learning_rate": 0.005,
    "critic_loss": "binary_crossentropy",
    "critic_l2_reg": 0.0001,

    "buffer_size": 2048,
    "train_size": 512,                                # train_size / batch_size burde være et heltall
    "batch_size": 64,
    "epochs": 1,

    "episodes": 2000,
    "save_frequency": 50,

    "mcts_starting_simulations": 140,
    "mcts_move_increase": 4,
    "mcts_increase_constant": 20,
    "mcts_move_decrease": 12,
    "mcts_decrease_constant": -10,

    "tournament_games": 40,                    # bør kunne deles på 8 for mest presise resultater
    "f": 0,
    "c": 4,
}


best_demo_config = {
    "episodes": 700,
    "save_frequency": 100,
    "size": 4,
    "tournament_games": 50,
    "f": 0,
    "actor_hidden_layers": [],
    "actor_activation": None,
}
