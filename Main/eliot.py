""" HER KAN ELIOT KØDDE LITT RUNDT """

from Main.config import config
from Tournaments.tournaments import Tournaments

tournaments = Tournaments(config)

names = ["hermine", "hermine"]

tournaments.run_elite_tournament(names=names)
