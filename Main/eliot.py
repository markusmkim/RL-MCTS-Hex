""" HER KAN ELIOT KØDDE LITT RUNDT """

from Main.config import config
from Tournaments.tournaments import Tournaments
from Agent.critic import Critic
from Main.utils import initialize_actor
import numpy as np

tournaments = Tournaments(config)

# nora = initialize_actor(config, name="nora")

# tournaments.run_one_vs_all(nora, randoms=19)

# names = ["last_model", "sylvester", "best_marco", "hermine", "henning", "arnold", "nils"]
# tournaments.run_elite_tournament(names=names, randoms=3)

tournaments.update_elite_evaluations()

# tournaments.run_topp_tournament()

# critic = Critic(name="nattaNils")

