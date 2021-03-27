config = {
    "size": 3,
    "starting_player": "alternate",
    "episodes": 100,
    "mcts_simulations": 400,  # 100
    "hidden_layers": [64, 32],
    "optimizer": 'adam',
    "activation_function": 'relu',
    "learning_rate": 0.0001,
    "loss": "cross_entropy",
    "training_frequency": 5,
    "training_probability": 0.5,
    "epsilon": 1,
    "epsilon_decay_rate": 0.97,
    "save_frequency": 20,
    "TOPP-G": 40,
    "c": 50,
}

""" 
Possible optimizers:        adam | sgd | rmsprop | adagrad 
Possible loss functions:    cross_entropy | mse | mae | kld
"""

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