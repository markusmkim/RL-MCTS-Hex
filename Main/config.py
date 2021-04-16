config = {
    "name": "gro",
    "train_from": False,
    "size": 6,

    "plot_evaluation_history": True,
    "visualize_last_game": False,
    "visualize_game_on_every_save": False,
    "run_interaction_game": False,

    "epsilon": 0.01,
    "epsilon_decay_rate": 1,
    "rollout_prob": 0,
    "min_rollout_prob": 1,
    "rollout_prob_decay_rate": 0,

    "actor_hidden_layers": [128, 128],
    "actor_optimizer": 'adam',
    "actor_activation": 'relu',
    "actor_learning_rate": 0.00002,
    "actor_loss": "mse",
    "actor_l2_reg": 0.0005,

    "rollout_actor":  False,
    "rollout_actor_episodes": 0,

    "use_critic": False,
    "critic_hidden_layers": [128, 64, 32],
    "critic_optimizer": 'adam',
    "critic_activation": 'relu',
    "critic_learning_rate": 0.0001,
    "critic_loss": "binary_crossentropy",
    "critic_l2_reg": 0.0001,

    "buffer_size": 2000,
    "train_size": 512,                                # train_size / batch_size burde være et heltall
    "batch_size": 64,
    "epochs": 1,

    "episodes": 300,
    "save_frequency": 20,

    "mcts_starting_simulations": 700,
    "mcts_move_increase": 4,
    "mcts_increase_constant": 10,
    "mcts_move_decrease": 22,
    "mcts_decrease_constant": 4,

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
