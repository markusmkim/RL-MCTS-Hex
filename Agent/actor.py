from tensorflow import keras
import numpy as np
import random
from Agent.utils import load_model, get_loss, get_optimizer


class Actor:
    def __init__(self, epsilon, epsilon_decay_rate,
                 input_dim=None, hidden_layers=None, optimizer=None,
                 activation_function=None, learning_rate=0, loss=None,
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
            self.model = load_model(name, count)
        else:
            self.model = self.build_model()


    def build_model(self):
        model = keras.Sequential()
        if len(self.hidden_layers) == 0:
            """ if no hidden layer, the output layer is the only layer """
            output_layer = (self.input_dim // 2) - 1  # must correspond to number of cells on board
            # add output layer with softmax
            model.add(keras.layers.Dense(output_layer, activation='softmax', input_shape=(self.input_dim,)))

        else:
            # add first hidden layer
            first_hidden_layer = self.hidden_layers[0]
            model.add(keras.layers.Dense(
                first_hidden_layer,
                activation=self.activation_function,
                input_shape=(self.input_dim,)))

            # add the rest of the hidden layers
            for layer in self.hidden_layers[1:]:
                model.add(keras.layers.Dense(layer, activation=self.activation_function))

            # add output layer, with softmax activation
            output_layer = (self.input_dim // 2) - 1  # must correspond to number of cells on board
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
            self.model.save(f"Agent/saved_models/{name}/network")
        else:
            self.model.save(f"Agent/saved_models/demo/network-{count}")


    def find_best_action(self, state):
        possible_actions = state[2]
        if len(possible_actions) == 0:
            return None

        if random.random() < self.epsilon:
            return possible_actions[random.randint(0, len(possible_actions) - 1)]

        output = np.array(self.model(state[0].reshape(1, len(state[0]))))

        best_action = np.argmax(output, axis=1)[0]
        while best_action not in possible_actions:
            output[0][best_action] = 0
            best_action = np.argmax(output, axis=1)[0]

        return best_action


    def decrease_epsilon(self):
        self.epsilon = self.epsilon * self.epsilon_decay_rate
