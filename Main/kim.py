""" HER KAN KIMMERN KØDDE LITT RUNDT """
from Agent.actor import Actor
from Agent.critic import Critic
from Main.config import config
from Tournaments.tournaments import Tournaments


tournaments = Tournaments(config)

tournaments.run_elite_tournament()

# a = Actor(0, 0, name="nora")
# critic = Critic(name="nora")

# tournaments.run_interaction_game(a, actor_starts=True, critic=critic)

