import numpy as np
import random
from Agent.utils import load_model, build_model


class Actor:
    def __init__(self, epsilon, epsilon_decay_rate,
                 input_dim=None, hidden_layers=None, optimizer=None,
                 activation=None, learning_rate=0, l2_reg=0, loss=None,
                 name=None, count=-1):

        self.input_dim = input_dim
        self.epsilon = epsilon
        self.epsilon_decay_rate = epsilon_decay_rate

        if name or count >= 0:
            self.model = load_model(name, count=count)
        else:
            self.model = build_model(hidden_layers, input_dim, activation, loss, optimizer, learning_rate, l2_reg)


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
            output[0][best_action] = -1
            best_action = np.argmax(output, axis=1)[0]

        return best_action


    def decrease_epsilon(self):
        self.epsilon = self.epsilon * self.epsilon_decay_rate
