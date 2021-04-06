config = {  # ikke kjørt denne enda
    "name": "marco",
    "size": 6,
    "starting_player": "alternate",

    "epsilon": 0.05,
    "epsilon_decay_rate": 1,

    "hidden_layers": [516, 256, 128],
    "optimizer": 'adam',
    "activation_function": 'relu',
    "learning_rate": 0.01,
    "loss": "mse",

    "training_probability": 0.8,
    "buffer_size": 96,                        # buffer_size / batch_size burde være et heltall
    "batch_size": 48,
    "epochs": 2,

    "episodes": 10,
    "save_frequency": 0,
    "mcts_simulations": 400,
    "mcts_discount_constant": 10,
    "mcts_discounted_simulations": 200,
    "tournament_games": 40,                   # bør kunne deles på 8 for mest presise resultater
    "c": 2,
}
