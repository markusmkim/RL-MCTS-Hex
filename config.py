config = {
    "size": 6,
    "starting_player": "alternate",
    "episodes": 200,
    "mcts_simulations": 100,  # 100
    "hidden_layers": [128, 64],
    "optimizer": 'adam',
    "activation_function": 'tanh',
    "learning_rate": 0.001,
    "training_frequency": 10,
    "training_probability": 0.5,
    "epsilon": 1,
    "epsilon_decay_rate": 0.98,
    "save_frequency": 20,
    "TOPP-G": 40,
    "c": 1,
}

"""
config = {
    "size": 4,
    "starting_player": "alternate",
    "episodes": 100,
    "mcts_simulations": 100,
    "hidden_layers": [60],
    "optimizer": 'sgd',
    "activation_function": 'relu',
    "learning_rate": 0.001,
    "training_frequency": 5,
    "training_probability": 0.5,
    "epsilon": 1,
    "epsilon_decay_rate": 0.97,
    "save_frequency": 10,
    "TOPP-G": 40,
    "c": 1,
}
"""