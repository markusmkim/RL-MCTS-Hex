config = {
    "name": "tull",
    "size": 6,

    "epsilon": 0.025,
    "epsilon_decay_rate": 1,
    "rollout_prob": 1,
    "min_rollout_prob": 0.2,
    "rollout_prob_decay_rate": 0.99,
    "training_probability": 0.8,

    "actor_hidden_layers": [256, 128, 64],
    "actor_optimizer": 'adam',
    "actor_activation": 'relu',
    "actor_learning_rate": 0.001,
    "actor_loss": "mse",
    "actor_l2_reg": 0.001,

    "critic_hidden_layers": [256, 128, 64],
    "critic_optimizer": 'adam',
    "critic_activation": 'relu',
    "critic_learning_rate": 0.001,
    "critic_loss": "binary_crossentropy",
    "critic_l2_reg": 0.001,

    "buffer_size": 128,                        # buffer_size / batch_size burde være et heltall
    "batch_size": 64,
    "epochs": 2,

    "episodes": 500,
    "save_frequency": 50,

    "mcts_starting_simulations": 50,
    "mcts_move_increase": 10,
    "mcts_increase_constant": 25,
    "mcts_move_decrease": 20,
    "mcts_decrease_constant": 10,
    "mcts_discounted_simulations": 50,

    "tournament_games": 8,                    # bør kunne deles på 8 for mest presise resultater
    "c": 4,
}
