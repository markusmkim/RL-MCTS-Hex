config = {
    "name": "hermine_v2",
    "size": 6,
    "starting_player": "alternate",
    "episodes": 1,
    "mcts_simulations": 450,
    "hidden_layers": [512, 256],
    "optimizer": 'adam',
    "activation_function": 'relu',
    "learning_rate": 0.008,
    "loss": "mse",
    "training_probability": 0.75,
    "buffer_size": 128,                # buffer_size / batch_size burde være et heltall
    "batch_size": 64,
    "epochs": 4,
    "epsilon": 0.05,
    "epsilon_decay_rate": 1,
    "save_frequency": None,
    "TOPP-G": 100,
    "c": 10,
    "mcts_discounted_simulations": 50,
    "mcts_discount_constant": 10,
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