from random import randint


class Actor:

    def find_next_move(self, possible_moves):
        if len(possible_moves) < 1:
            return None

        index = randint(0, len(possible_moves) - 1)
        return possible_moves[index]


