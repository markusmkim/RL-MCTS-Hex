a1 = {
    "name": "a1",
    "size": 6,
    "train_from_actor": False,
    "train_from_critic": False,

    "epsilon": 1,
    "epsilon_decay_rate": 1,

    "actor_hidden_layers": [512, 512],
    "actor_optimizer": 'adam',
    "actor_activation": 'relu',
    "actor_learning_rate": 0.001,
    "actor_loss": "mae",
    "actor_l2_reg": 0.000001,
}

a2 = {
    "name": "a2",
    "size": 6,
    "train_from_actor": False,
    "train_from_critic": False,

    "epsilon": 1,
    "epsilon_decay_rate": 1,

    "actor_hidden_layers": [512, 512],
    "actor_optimizer": 'adam',
    "actor_activation": 'relu',
    "actor_learning_rate": 0.0012,
    "actor_loss": "mae",
    "actor_l2_reg": 0.000001,
}

a3 = {
    "name": "a3",
    "size": 6,
    "train_from_actor": False,
    "train_from_critic": False,

    "epsilon": 1,
    "epsilon_decay_rate": 1,

    "actor_hidden_layers": [512, 512],
    "actor_optimizer": 'adam',
    "actor_activation": 'relu',
    "actor_learning_rate": 0.0005,
    "actor_loss": "mae",
    "actor_l2_reg": 0.000001,
}

a4 = {
    "name": "a4",
    "size": 6,
    "train_from_actor": False,
    "train_from_critic": False,

    "epsilon": 1,
    "epsilon_decay_rate": 1,

    "actor_hidden_layers": [720, 720],
    "actor_optimizer": 'adam',
    "actor_activation": 'relu',
    "actor_learning_rate": 0.001,
    "actor_loss": "mae",
    "actor_l2_reg": 0.000001,
}

a5 = {
    "name": "a5",
    "size": 6,
    "train_from_actor": False,
    "train_from_critic": False,

    "epsilon": 1,
    "epsilon_decay_rate": 1,

    "actor_hidden_layers": [256, 512, 256],
    "actor_optimizer": 'adam',
    "actor_activation": 'relu',
    "actor_learning_rate": 0.001,
    "actor_loss": "mae",
    "actor_l2_reg": 0.000001,
}

a6 = {
    "name": "a6",
    "size": 6,
    "train_from_actor": False,
    "train_from_critic": False,

    "epsilon": 1,
    "epsilon_decay_rate": 1,

    "actor_hidden_layers": [256, 128],
    "actor_optimizer": 'adam',
    "actor_activation": 'relu',
    "actor_learning_rate": 0.001,
    "actor_loss": "mae",
    "actor_l2_reg": 0.000001,
}

a7 = {
    "name": "nanna_v2",
    "size": 6,
    "train_from_actor": "old_nanna",
    "train_from_critic": False,

    "epsilon": 1,
    "epsilon_decay_rate": 1,

    "actor_hidden_layers": [512, 512],
    "actor_optimizer": 'adam',
    "actor_activation": 'relu',
    "actor_learning_rate": 0.001,
    "actor_loss": "mae",
    "actor_l2_reg": 0.000001,
}