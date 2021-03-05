from random import randint, random
import tensorflow as tf
from tensorflow import keras
import numpy as np


class Actor:

    def __init__(self, input_dim, hidden_layers, learning_rate, epsilon, epsilon_decay_rate):
        self.input_dim = input_dim
        self.hidden_layers = hidden_layers
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.epsilon_decay_rate = epsilon_decay_rate
        self.model = self.build_model()


    def build_model(self):
        model = keras.Sequential()
        if len(self.hidden_layers) == 0:
            output_layer = 16  # number must correspond to number of cells on board (number of "categories")
            # add output layer with softmax
            model.add(keras.layers.Dense(output_layer, activation='softmax', input_shape=(self.input_dim,)))

        else:
            # add first hidden layer
            first_hidden_layer = self.hidden_layers[0]
            model.add(keras.layers.Dense(first_hidden_layer, activation='relu', input_shape=(self.input_dim,)))

            # add the rest of the hidden layers
            for layer in self.hidden_layers[1:]:
                model.add(keras.layers.Dense(layer, activation='relu'))

            # add output layer, with softmax activation
            output_layer = 16  # number must correspond to number of cells on board (number of "categories")
            model.add(keras.layers.Dense(output_layer, activation='softmax'))

        loss = keras.losses.CategoricalCrossentropy()                           # use crossentropy loss function
        optimizer = keras.optimizers.Adam(learning_rate=self.learning_rate)     # use Adam optimizer
        model.compile(optimizer=optimizer, loss=loss)
        print(model.summary())
        return model


    def train_model(self, x_train, y_train):
        self.model.fit(x_train, y_train, verbose=0)  # verbose = 0 to run silent (no prints to console while training)


    def find_best_action(self, state):
        return self.model(state)


    def decrease_epsilon(self):
        self.epsilon = self.epsilon * self.epsilon_decay_rate


a = Actor(17, [50, 10], 0.01, 0.5, 0.999)
input_data_test = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]])
print(a.find_best_action(input_data_test))
