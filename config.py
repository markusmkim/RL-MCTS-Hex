config = {
    "name": "nanna",
    "size": 6,
    "starting_player": "alternate",

    "epsilon": 0.05,
    "epsilon_decay_rate": 1,

    "hidden_layers": [544, 128],
    "optimizer": 'adam',
    "activation_function": 'relu',
    "learning_rate": 0.005,
    "loss": "mse",

    "training_probability": 0.75,
    "buffer_size": 96,                # buffer_size / batch_size burde være et heltall
    "batch_size": 48,
    "epochs": 4,

    "episodes": 10,
    "save_frequency": 20,
    "mcts_simulations": 20,
    "mcts_discounted_simulations": 10,
    "mcts_discount_constant": 0,
    "TOPP-G": 20,
    "c": 10,
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