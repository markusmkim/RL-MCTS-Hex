config = {
    "name": "demo",
    "size": 4,

    "epsilon": 0.05,
    "epsilon_decay_rate": 1,
    "rollout_prob": 1,
    "min_rollout_prob": 0.2,
    "rollout_prob_decay_rate": 1,

    "actor_hidden_layers": [64, 64],
    "actor_optimizer": 'adam',
    "actor_activation": 'relu',
    "actor_learning_rate": 0.001,
    "actor_loss": "mse",
    "actor_l2_reg": 0.0001,

    "critic_hidden_layers": [256, 128, 64],
    "critic_optimizer": 'adam',
    "critic_activation": 'relu',
    "critic_learning_rate": 0.00001,
    "critic_loss": "binary_crossentropy",
    "critic_l2_reg": 0.0001,

    "buffer_size": 128,                        # buffer_size / batch_size burde være et heltall
    "batch_size": 64,
    "epochs": 1,

    "episodes": 200,
    "save_frequency": 50,

    "mcts_starting_simulations": 3,
    "mcts_move_increase": 2,
    "mcts_increase_constant": 0,
    "mcts_move_decrease": 12,
    "mcts_decrease_constant": 0,

    "tournament_games": 40,                    # bør kunne deles på 8 for mest presise resultater
    "c": 3,
}
