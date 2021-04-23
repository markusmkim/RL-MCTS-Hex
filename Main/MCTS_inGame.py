from Main.config import config
from Tournaments.tournaments import Tournaments
from Agent.actor import Actor
from Tournaments.OHT.oht_actor import OhtActor

a = Actor(0, 0, randomized=True)

nora_v2 = Actor(0, 0, name="groverud")

oht_actor = OhtActor()

t = Tournaments(config)

t.run_duel(nora_v2, oht_actor, 6, actor2_runs_mcts=True, oht_actor_as_actor2=True)
# t.run_interaction_game(a, actor_starts=True)

