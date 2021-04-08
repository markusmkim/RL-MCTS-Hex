""" HER KAN KIMMERN KØDDE LITT RUNDT """
from Agent.actor import Actor
from Main.config import config
from Tournaments.tournaments import Tournaments

tournaments = Tournaments(config)
# tournaments.run_elite_tournament()

emma = Actor(0, 0, name="emma")
tournaments.run_interaction_game(emma, actor_starts=True)
