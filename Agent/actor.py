import tensorflow as tf
from tensorflow import keras
import numpy as np
import random


class Actor:
    def __init__(self, epsilon, epsilon_decay_rate,
                 input_dim=None, hidden_layers=None, optimizer=None, activation_function=None, learning_rate=0, loss=None,
                 name=None, count=-1):
        self.input_dim = input_dim
        self.hidden_layers = hidden_layers
        self.learning_rate = learning_rate
        self.loss = loss
        self.optimizer = optimizer
        self.activation_function = activation_function
        self.epsilon = epsilon
        self.epsilon_decay_rate = epsilon_decay_rate
        if name or count >= 0:
            self.model = self.load_model(name, count)
        else:
            self.model = self.build_model()


    def build_model(self):
        model = keras.Sequential()
        if len(self.hidden_layers) == 0:
            """ if no hidden layer, the output layer is the only layer """
            output_layer = (self.input_dim // 2) - 1  # must correspond to number of cells on board (number of "categories")
            # add output layer with softmax
            model.add(keras.layers.Dense(output_layer, activation='softmax', input_shape=(self.input_dim,)))

        else:
            # add first hidden layer
            first_hidden_layer = self.hidden_layers[0]
            model.add(keras.layers.Dense(first_hidden_layer, activation=self.activation_function, input_shape=(self.input_dim,)))

            # add the rest of the hidden layers
            for layer in self.hidden_layers[1:]:
                model.add(keras.layers.Dense(layer, activation=self.activation_function))

            # add output layer, with softmax activation
            output_layer = (self.input_dim // 2) - 1  # must correspond to number of cells on board (number of "categories")
            model.add(keras.layers.Dense(output_layer, activation='softmax'))

        loss = get_loss(self.loss)
        # print(loss)
        optimizer = get_optimizer(self.optimizer, self.learning_rate)
        model.compile(optimizer=optimizer, loss=loss)
        return model


    def train_model(self, x_train, y_train, batch_size, epochs):
        self.model.fit(np.array(x_train), np.array(y_train),
                       batch_size=batch_size,
                       epochs=epochs,
                       verbose=0)  # verbose = 0 to run silent


    def save_model(self, name, count=-1):
        if count == -1:
            self.model.save(f"Agent/saved_models/{name}/network.h5")
        else:
            self.model.save(f"Agent/saved_models/demo/network-{count}.h5")


    def load_model(self, name, count=-1):
        if count == -1:
            return keras.models.load_model(f"Agent/saved_models/{name}/network.h5")
        else:
            return keras.models.load_model(f"Agent/saved_models/demo/network-{count}.h5")


    def find_best_action(self, state):
        possible_actions = state[2]
        if len(possible_actions) == 0:
            return None

        if random.random() < self.epsilon:
            return possible_actions[random.randint(0, len(possible_actions) - 1)]

        output = np.array(self.model(state[0].reshape(1, len(state[0]))))
        # print(output)
        best_action = np.argmax(output, axis=1)[0]
        while best_action not in possible_actions:
            output[0][best_action] = 0
            best_action = np.argmax(output, axis=1)[0]

        return best_action


    def decrease_epsilon(self):
        self.epsilon = self.epsilon * self.epsilon_decay_rate


    # Old methods
    def load_weights(self, path):
        self.model.load_weights(path).expect_partial()


    def save_weights(self, path):
        self.model.save_weights(path)


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


""" Testing 


input_data_test = np.array([
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 1, 1, 1, 0, 0, 0, 0]
])

targets_data_test = np.array([
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
])

a = Actor(17, [50, 10], 0.001, 0.5, 0.999)
a.train_model(input_data_test, targets_data_test, epochs=200)
outputs_a = a.find_best_action(input_data_test)
print('\nEvaluate-----------------------------------------------------------------------------------------------------')
print('\nPredictions trained model', np.argmax(outputs_a, axis=1) + 1)
a.model.evaluate(input_data_test, targets_data_test, verbose=2)

# load saved models
model = 1
for i in range(50, 201, 50):
    print(f'\n Saved model {model}')
    b = Actor(17, [50, 10], 0.001, 0.5, 0.999)
    b.load_weights(f"saved_networks/cp-{i:04d}.ckpt")
    outputs_b = b.find_best_action(input_data_test)
    print('Predictions', np.argmax(outputs_b, axis=1) + 1)
    b.model.evaluate(input_data_test, targets_data_test, verbose=2)
    model += 1
"""