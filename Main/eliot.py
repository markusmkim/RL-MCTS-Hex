""" HER KAN ELIOT KØDDE LITT RUNDT """

from Main.config import config
from Tournaments.tournaments import Tournaments

tournaments = Tournaments(config)

# names = ["last_model", "sylvester", "best_marco", "hermine", "henning", "arnold", "nils"]
# tournaments.run_elite_tournament(names=names, randoms=3)

tournaments.update_elite_evaluations()
