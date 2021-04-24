from Main.config import config
from Tournaments.tournaments import Tournaments
from Agent.actor import Actor


a = Actor(0, 0, randomized=True)

nora_v2 = Actor(0, 0, name="groverud")


t = Tournaments(config)

t.run_duel(nora_v2, a, 6, actor2_runs_mcts=True)
# t.run_interaction_game(a, actor_starts=True)

