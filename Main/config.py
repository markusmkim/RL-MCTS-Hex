config = {
    "name": "sjur",
    "size": 4,
    "train_from_actor": False,
    "train_from_critic": False,

    "plot_evaluation_history": True,
    "visualize_last_game": False,
    "visualize_game_on_every_save": False,
    "run_interaction_game": False,

    "epsilon": 1,
    "epsilon_decay_rate": 1,
    "rollout_prob": 1,
    "min_rollout_prob": 1,
    "rollout_prob_decay_rate": 1,

    "actor_hidden_layers": [80, 80],
    "actor_optimizer": 'adam',
    "actor_activation": 'relu',
    "actor_learning_rate": 0.005,
    "actor_loss": "mse",
    "actor_l2_reg": 0.0001,

    "rollout_actor":  False,
    "rollout_actor_episodes": 0,

    "use_critic": False,
    "train_critic": False,
    "critic_hidden_layers": [256, 128, 64],
    "critic_optimizer": 'adam',
    "critic_activation": 'relu',
    "critic_learning_rate": 0.001,
    "critic_loss": "binary_crossentropy",
    "critic_l2_reg": 0.0001,

    "buffer_size": 1024,
    "train_size": 512,                                # train_size / batch_size burde være et heltall
    "batch_size": 64,
    "epochs": 1,

    "episodes": 200,
    "save_frequency": 20,

    "mcts_starting_simulations": 0,
    "mcts_move_increase": 0,
    "mcts_increase_constant": 0,
    "mcts_move_decrease": 0,
    "mcts_decrease_constant": 0,

    "tournament_games": 40,                    # bør kunne deles på 8 for mest presise resultater
    "c": 3,
}


best_demo_config = {
    "episodes": 700,
    "save_frequency": 100,
    "size": 4,
    "tournament_games": 50,
    "actor_hidden_layers": [],
    "actor_activation": None,
}
