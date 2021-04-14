from Main.config import best_demo_config
from Agent.actor import Actor
from Tournaments.tournaments import Tournaments

tournament = Tournaments(best_demo_config)

tournament.run_topp_tournament(plot=True, best=True)

best_actor = Actor(0, 0, name="bestDemoAgent")

win_rate = tournament.run_one_vs_all(best_actor, display=False)
print("Actor won", win_rate, "% of games against fully randomized agents!")


# tournament.run_duel(best_actor, "random", 4)
