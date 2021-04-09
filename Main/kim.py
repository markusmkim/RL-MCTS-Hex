""" HER KAN KIMMERN KØDDE LITT RUNDT """
from Agent.actor import Actor
from Agent.critic import Critic
from Main.config import config
from Tournaments.tournaments import Tournaments
from SimWorld.utils import generate_board, visualize_board
import numpy as np

tournaments = Tournaments(config)
# tournaments.run_elite_tournament()

emma = Actor(0, 0, name="emma")
critic = Critic(name="demo")
tournaments.run_interaction_game(emma, actor_starts=True, critic=critic)


"""
grid = [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0,
        0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0,
        0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0,
        0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]

inp = [0, 1] + grid

#visualize_board(generate_board(grid))

#print(critic.test_evaluate(np.array(inp)))

"""
