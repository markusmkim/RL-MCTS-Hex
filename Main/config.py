config = {
    "name": "salah",
    "size": 6,

    "epsilon": 0.025,
    "epsilon_decay_rate": 1,
    "rollout_prob": 0,
    "min_rollout_prob": 1,
    "rollout_prob_decay_rate": 0,

    "actor_hidden_layers": [256, 128, 64],
    "actor_optimizer": 'adam',
    "actor_activation": 'relu',
    "actor_learning_rate": 0.001,
    "actor_loss": "mse",
    "actor_l2_reg": 0.0001,

    "critic_hidden_layers": [128, 64, 32],
    "critic_optimizer": 'adam',
    "critic_activation": 'relu',
    "critic_learning_rate": 0.0001,
    "critic_loss": "binary_crossentropy",
    "critic_l2_reg": 0.0001,

    "buffer_size": 2048,                        # buffer_size / batch_size burde være et heltall
    "batch_size": 64,
    "epochs": 1,

    "episodes": 100,
    "save_frequency": 50,

    "mcts_starting_simulations": 20,
    "mcts_move_increase": 16,
    "mcts_increase_constant": 5,
    "mcts_move_decrease": 24,
    "mcts_decrease_constant": 2,

    "tournament_games": 40,                    # bør kunne deles på 8 for mest presise resultater
    "c": 3,
}
