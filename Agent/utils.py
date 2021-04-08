from tensorflow import keras


def build_model(hidden_layers, input_dim, activation, loss, optimizer, learning_rate, l2_reg, critic=False, akimbo=False):
    model = keras.Sequential()
    output_activation = "tanh" if critic else "softmax"
    output_layer = 1 if critic else (input_dim // 2) if akimbo else (input_dim // 2) - 1
    reg = keras.regularizers.l2(l2=l2_reg)

    if len(hidden_layers) == 0:
        """ if no hidden layer, the output layer is the only layer """
        model.add(keras.layers.Dense(output_layer, activation=output_activation, input_shape=(input_dim,), kernel_regularizer=reg))

    else:
        # add first hidden layer
        first_hidden_layer = hidden_layers[0]
        model.add(keras.layers.Dense(
            first_hidden_layer,
            activation=activation,
            input_shape=(input_dim,)))

        # add the rest of the hidden layers
        for layer in hidden_layers[1:]:
            model.add(keras.layers.Dense(layer, activation=activation, kernel_regularizer=reg))

        model.add(keras.layers.Dense(output_layer, activation=output_activation, kernel_regularizer=reg))

    loss = get_loss(loss)
    optimizer = get_optimizer(optimizer, learning_rate)
    model.compile(optimizer=optimizer, loss=loss)
    return model


def load_model(name, critic=False, count=-1, color=None):
    if critic:
        return keras.models.load_model(f"Agent/saved_critics/{name}/network")

    if color:
        if count == -1:
            return keras.models.load_model(f"Agent/saved_models/{name}/{color}/network")
        else:
            return keras.models.load_model(f"Agent/saved_models/demo/{color}/network-{count}")
    else:
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