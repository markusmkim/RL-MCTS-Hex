""" HER KAN ELIOT KØDDE LITT RUNDT """

from Main.config import config
from Tournaments.tournaments import Tournaments

tournaments = Tournaments(config)

names = ["last_model", "sylvester", "best_nils", "hermine", "henning", "arnold", "nils"]

tournaments.run_elite_tournament(names=names, randoms=3)
