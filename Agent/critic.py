import numpy as np
from Agent.utils import build_model


class Critic:
    def __init__(self,
                 input_dim=None, hidden_layers=None, optimizer=None,
                 activation=None, learning_rate=0, l2_reg=0, loss=None):

        self.model = build_model(hidden_layers, input_dim, activation, loss, optimizer, learning_rate, l2_reg, critic=True)


    def train_model(self, x_train, y_train, batch_size, epochs):
        self.model.fit(np.array(x_train), np.array(y_train),
                       batch_size=batch_size,
                       epochs=epochs,
                       verbose=0)  # verbose = 0 to run silent


    def evaluate(self, state):
        return self.model(state[0].reshape(1, len(state[0])))


    def save_model(self, name):
        self.model.save(f"Agent/saved_critics/{name}/network")
