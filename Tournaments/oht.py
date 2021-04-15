""" Main for OHT """

from BasicClientActor import BasicClientActor

basicClientActor = BasicClientActor()

state = [2, 0, 1, 1, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 1, 0,
         0, 1, 1, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0]

print(basicClientActor.handle_get_action(state))
