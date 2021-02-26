

class Player:
    def __init__(self, pid, board):
        self.board = board
        self.pid = pid


    def get_possible_moves(self):
        return self.board.get_possible_moves()


    def make_move(self, move):
        # print(move)
        self.board.move(move)

        """
        if self.board.is_game_over():
            return [0, self.pid], 1

        stones = self.board.stones
        """
