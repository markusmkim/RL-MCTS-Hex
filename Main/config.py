config = {
    "name": "emma_v2",
    "size": 6,

    "epsilon": 0.05,
    "epsilon_decay_rate": 1,
    "rollout_prob": 1,
    "rollout_prob_decay_rate": 0.98,
    "training_probability": 0.8,

    "hidden_layers": [256, 128, 64],
    "optimizer": 'adam',
    "activation": 'relu',
    "learning_rate": 0.01,
    "loss": "mse",
    "l2_reg": 0.003,

    "buffer_size": 128,                        # buffer_size / batch_size burde være et heltall
    "batch_size": 64,
    "epochs": 2,

    "episodes": 100,
    "save_frequency": 20,
    "mcts_simulations": 600,
    "mcts_discount_constant": 10,
    "mcts_discounted_simulations": 60,
    "tournament_games": 40,                    # bør kunne deles på 8 for mest presise resultater
    "c": 2,
}
