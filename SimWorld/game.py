from SimWorld.board import NimBoard
from SimWorld.player import Player


board = NimBoard(45, 5, 0)

p0 = Player(0, board)
p1 = Player(1, board)

winner = -1

while not board.is_game_over():
    possible_moves = board.get_possible_moves()
    print(possible_moves)
    action = possible_moves[0]
    if board.next_player == 0:
        p0.make_move(action)
        if board.is_game_over():
            winner = 0

    else:
        p1.make_move(action)
        if board.is_game_over():
            winner = 1

print('Winner: ', winner)
