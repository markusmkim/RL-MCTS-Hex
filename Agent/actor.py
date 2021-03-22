import tensorflow as tf
from tensorflow import keras
import numpy as np
import random


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
            """ if no hidden layer, the output layer is the only layer """
            output_layer = (self.input_dim // 2) - 1  # must correspond to number of cells on board (number of "categories")
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
            output_layer = (self.input_dim // 2) - 1  # must correspond to number of cells on board (number of "categories")
            model.add(keras.layers.Dense(output_layer, activation='softmax'))

        loss = keras.losses.CategoricalCrossentropy()                           # use crossentropy loss function
        # optimizer = keras.optimizers.Adam(learning_rate=self.learning_rate)     # use Adam optimizer
        optimizer = keras.optimizers.SGD(learning_rate=self.learning_rate) # SGD
        model.compile(optimizer=optimizer, loss=loss)
        # print(model.summary())
        return model


    def train_model(self, x_train, y_train, epochs=1, count=-1):
        if count == -1:
            self.model.fit(np.array(x_train), np.array(y_train), epochs=epochs,
                           verbose=0)  # verbose = 0 to run silent
            return

        print('Saving')
        checkpoint_path = f"Agent/saved_networks/cp-{count}.ckpt"
        # Create a callback that saves the model's weights
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                         save_weights_only=True,
                                                         verbose=1,
                                                         save_freq=1)

        # verbose = 0 to run silent
        self.model.fit(np.array(x_train), np.array(y_train), callbacks=[cp_callback], epochs=epochs, verbose=0)


    def load_weights(self, path):
        self.model.load_weights(path).expect_partial()


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