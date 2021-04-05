

# player 1 = (1, 0) = black --> has the north-west and south-east sides
# player 2 = (0, 1) = red   --> has the north-east and south-west sides
def get_winner_old(self):

    # try to find a winning chain for black (player 1)
    possible_chains = []
    for i in range(len(self.board)):
        if self.board[0][i] == 1:
            possible_chains.append(i)

    for i in range(1, len(self.board)):
        next_possible_chains = []
        for cell in possible_chains:
            if self.board[i][cell] == 1:
                next_possible_chains.append(cell)
            if cell < len(self.board) - 1:
                if self.board[i][cell + 1] == 1:
                    next_possible_chains.append(cell + 1)

        possible_chains = next_possible_chains

    if len(possible_chains) > 0:
        return 1

    # try to find a winning chain for red (player 2)
    possible_chains = []
    for i in range(len(self.board)):
        if self.board[i][0] == 2:
            possible_chains.append(i)

    for i in range(1, len(self.board)):
        next_possible_chains = []
        for cell in possible_chains:
            if self.board[cell][i] == 2:
                next_possible_chains.append(cell)
            if cell < len(self.board) - 1:
                if self.board[cell + 1][i] == 2:
                    next_possible_chains.append(cell + 1)
        possible_chains = next_possible_chains

    if len(possible_chains) > 0:
        return 2

    return 0


# Old methods
def load_weights(self, path):
    self.model.load_weights(path).expect_partial()


def save_weights(self, path):
    self.model.save_weights(path)


"""
||| HENTET FRA CONFIG |||

Possible optimizers:        adam | sgd | rmsprop | adagrad 
Possible loss functions:    cross_entropy | mse | mae | kld


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

"""
||| HENTET FRA ACTOR |||

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


"""
||| HENTET FRA GAMLE DEBUGGER |||

game_manager = HexManager([1, 0], 4)

while not game_manager.is_game_over():
    possible_actions = game_manager.get_state()[2]
    if len(possible_actions) == 0:
        break
    old_board = copy.deepcopy(game_manager.board)
    game_manager.execute_action(possible_actions[randint(0, len(possible_actions) - 1)])

winner = game_manager.get_winner()
print(winner)
# print(game_manager.get_state())
# game_manager.printChains()
# game_manager.visualize_game_state()
if winner > 0:                              # når en har vunnet
    visualize_board(old_board)              # print siste state før seier
    sleep(1)
    game_manager.visualize_game_state()     # print state hvor en har seiret


print("")

print(game_manager.execute_action(9))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()

print("")

print(game_manager.execute_action(3))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()

print("")

print(game_manager.execute_action(6))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()


print("")

print(game_manager.execute_action(4))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()


print("")

print(game_manager.execute_action(1))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()


print("")

print(game_manager.execute_action(15))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()

print("")

print(game_manager.execute_action(13))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()

print("")

print(game_manager.execute_action(0))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()

print("")

print(game_manager.execute_action(8))
print(game_manager.get_state())
game_manager.printChains()
game_manager.visualize_game_state()
"""
"""
black_1 = [[2, 1, 2], [2, 1, 1], [2, 1, 2]]
black_2 = [[1, 2, 1], [1, 1, 2], [2, 1, 2]]
black_3 = [[2, 2, 2], [2, 2, 2], [2, 2, 2]]

red_1 = [[2, 2, 1], [2, 2, 2], [1, 1, 1]]
red_2 = [[1, 1, 2], [2, 2, 1], [2, 1, 2]]
red_3 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

bingo = [[2, 1, 1, 2], [1, 2, 1, 2], [1, 1, 1, 1], [2, 1, 1, 1]]

visualize_board(bingo)
"""
