config = {
    "name": "akimboNils",
    "size": 4,

    "epsilon": 0.05,
    "epsilon_decay_rate": 1,

    "hidden_layers": [128, 64, 32],
    "optimizer": 'adam',
    "activation_function": 'relu',
    "learning_rate": 0.005,
    "loss": "mae",

    "training_probability": 0.8,
    "buffer_size": 64,                        # buffer_size / batch_size burde være et heltall
    "batch_size": 32,
    "epochs": 2,

    "episodes": 150,
    "save_frequency": 10,
    "mcts_simulations": 100,
    "mcts_discount_constant": 5,
    "mcts_discounted_simulations": 40,
    "tournament_games": 40,                    # bør kunne deles på 8 for mest presise resultater
    "c": 2,
}
