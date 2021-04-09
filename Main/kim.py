""" HER KAN KIMMERN KØDDE LITT RUNDT """
from Agent.actor import Actor
from Agent.critic import Critic
from Main.config import config
from Tournaments.tournaments import Tournaments


tournaments = Tournaments(config)

emma = Actor(0, 0, name="emma")
critic = Critic(name="triana")

tournaments.run_interaction_game(emma, actor_starts=True, critic=critic)

