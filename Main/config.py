config = {
    "name": "huhu",
    "size": 6,
    "train_from_actor": False,
    "train_from_critic": False,

    "plot_evaluation_history": True,
    "visualize_last_game": False,
    "visualize_game_on_every_save": False,
    "run_interaction_game": False,

    "epsilon": 0.01,
    "epsilon_decay_rate": 1,
    "rollout_prob": 5,
    "min_rollout_prob": 0.3,
    "rollout_prob_decay_rate": 0.8,

    "actor_hidden_layers": [256, 128, 64],
    "actor_optimizer": 'adam',
    "actor_activation": 'relu',
    "actor_learning_rate": 0.005,
    "actor_loss": "mse",
    "actor_l2_reg": 0.0001,

    "rollout_actor":  False,
    "rollout_actor_episodes": 0,

    "use_critic": True,
    "train_critic": True,
    "critic_hidden_layers": [256, 128, 64],
    "critic_optimizer": 'adam',
    "critic_activation": 'relu',
    "critic_learning_rate": 0.005,
    "critic_loss": "binary_crossentropy",
    "critic_l2_reg": 0.0001,

    "buffer_size": 1024,
    "train_size": 256,                                # train_size / batch_size burde være et heltall
    "batch_size": 64,
    "epochs": 1,

    "episodes": 40,
    "save_frequency": 10,

    "mcts_starting_simulations": 2,
    "mcts_move_increase": 5,
    "mcts_increase_constant": 0,
    "mcts_move_decrease": 25,
    "mcts_decrease_constant": 0,

    "tournament_games": 8,                    # bør kunne deles på 8 for mest presise resultater
    "c": 4,
}


best_demo_config = {
    "episodes": 700,
    "save_frequency": 100,
    "size": 4,
    "tournament_games": 50,
    "actor_hidden_layers": [],
    "actor_activation": None,
}
