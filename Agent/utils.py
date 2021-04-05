from tensorflow import keras


def load_model(name, count=-1):
    if count == -1:
        return keras.models.load_model(f"Agent/saved_models/{name}/network")
    else:
        return keras.models.load_model(f"Agent/saved_models/demo/network-{count}")


def get_loss(name):
    """
    Returns loss with given name.
    If name is invalid, function will return MSE as default.
    Valid options: cross_entropy | mse | mae | kld
    """
    if name == "cross_entropy":
        return keras.losses.CategoricalCrossentropy()
    if name == "kld":
        return keras.losses.KLDivergence()
    if name == "mae":
        return keras.losses.MeanAbsoluteError()
    return keras.losses.MeanSquaredError()


def get_optimizer(name, learning_rate):
    """
    Returns optimizer with given name.
    If name is invalid, function will return SGD as default.
    Valid options: adagrad | rmsprop | adam | sgd
    """
    if name == 'adagrad':
        return keras.optimizers.Adagrad(learning_rate=learning_rate)
    if name == 'rmsprop':
        return keras.optimizers.RMSprop(learning_rate=learning_rate)
    if name == 'adam':
        return keras.optimizers.Adam(learning_rate=learning_rate)

    return keras.optimizers.SGD(learning_rate=learning_rate)