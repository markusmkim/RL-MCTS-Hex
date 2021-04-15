config = {
    "name": "demo",
    "train_from": False,
    "size": 4,

    "plot_evaluation_history": False,
    "visualize_last_game": True,
    "visualize_game_on_every_save": False,
    "run_interaction_game": False,

    "epsilon": 0.01,
    "epsilon_decay_rate": 1,
    "rollout_prob": 0,
    "min_rollout_prob": 1,
    "rollout_prob_decay_rate": 0,

    "actor_hidden_layers": [256, 128, 64],
    "actor_optimizer": 'adam',
    "actor_activation": 'relu',
    "actor_learning_rate": 0.002,
    "actor_loss": "mse",
    "actor_l2_reg": 0.001,

    "rollout_actor":  False,
    "rollout_actor_episodes": 0,

    "use_critic": False,
    "critic_hidden_layers": [128, 64, 32],
    "critic_optimizer": 'adam',
    "critic_activation": 'relu',
    "critic_learning_rate": 0.0001,
    "critic_loss": "binary_crossentropy",
    "critic_l2_reg": 0.0001,

    "buffer_size": 1000,
    "train_size": 512,                                # train_size / batch_size burde være et heltall
    "batch_size": 32,
    "epochs": 1,

    "episodes": 3,
    "save_frequency": 20,

    "mcts_starting_simulations": 10,
    "mcts_move_increase": 4,
    "mcts_increase_constant": 0,
    "mcts_move_decrease": 16,
    "mcts_decrease_constant": 0,

    "tournament_games": 40,                    # bør kunne deles på 8 for mest presise resultater
    "f": 0,
    "c": 2,
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
