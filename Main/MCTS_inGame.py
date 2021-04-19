from time import time
from Main.config import config
from Tournaments.tournaments import Tournaments
from SimWorld.utils import visualize_game
from Main.utils import plot_histories, initialize_actor, initialize_critic, save_metadata, save_elites, read_elites, evaluate_progression
from RL.algorithm import run_rl_algorithm
from Agent.actor import Actor

a = Actor(0, 0, randomized=True)

nora_v2 = Actor(0, 0, name="emma")

t = Tournaments(config)

t.run_duel(nora_v2, a, 6, actor2_runs_mcts=True)
# t.run_interaction_game(a, actor_starts=True)

