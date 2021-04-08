config = {
    "name": "madonna",
    "size": 6,

    "epsilon": 0.05,
    "epsilon_decay_rate": 1,
    "rollout_prob": 0,
    "rollout_prob_decay_rate": 1,
    "training_probability": 0.8,

    "hidden_layers": [128, 64],
    "optimizer": 'adam',
    "activation": 'relu',
    "learning_rate": 0.005,
    "loss": "mae",
    "l2_reg": 0.001,

    "buffer_size": 64,                        # buffer_size / batch_size burde være et heltall
    "batch_size": 32,
    "epochs": 2,

    "episodes": 10,
    "save_frequency": 10,
    "mcts_simulations": 20,
    "mcts_discount_constant": 0,
    "mcts_discounted_simulations": 40,
    "tournament_games": 40,                    # bør kunne deles på 8 for mest presise resultater
    "c": 2,
}
