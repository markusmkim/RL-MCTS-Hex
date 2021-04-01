config = {
    "name": "silje",
    "size": 6,
    "starting_player": "alternate",
    "episodes": 100,
    "mcts_simulations": 400,
    "hidden_layers": [512, 64],
    "optimizer": 'adam',
    "activation_function": 'relu',
    "learning_rate": 0.02,
    "loss": "mse",
    "training_probability": 0.8,
    "buffer_size": 64,                # buffer_size / batch_size burde være et heltall
    "batch_size": 32,
    "epochs": 5,
    "epsilon": 1,
    "epsilon_decay_rate": 0.9,
    "save_frequency": None,
    "TOPP-G": 100,
    "c": 1.5,
    "mcts_discounted_simulations": 120,
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