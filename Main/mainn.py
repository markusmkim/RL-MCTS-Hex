from time import time
from Main.config import config
from Tournaments.tournaments import Tournaments
from SimWorld.utils import visualize_game
from Main.utils import plot_history, initialize_actor, initialize_critic
from Main.utils import save_metadata, save_elites, read_elites
from RL.algorithm import run_rl_algorithm

print("Welcome to a game of Hex!")

actor = initialize_actor(config, config["train_from_actor"])
critic = initialize_critic(config, config["train_from_critic"]) if config["use_critic"] else False

print("Actor initialized")

tournaments = Tournaments(config)
start_time = time()

evaluation_history, last_game_history, saved_actor_count, rph = run_rl_algorithm(actor, critic, config, tournaments)

if config["use_critic"]:
    critic.save_model(config["name"])

time_spent = time() - start_time
print("Time spent on entire run:", time_spent)
print("")

if config["plot_evaluation_history"] and len(evaluation_history) > 0:
    plot_history(evaluation_history, config["save_frequency"])
    plot_history(rph, config["save_frequency"])

if config["visualize_last_game"]:
    visualize_game(last_game_history)


print("Setting actor's epsilon to 0")
actor.epsilon = 0

if config["run_interaction_game"]:
    tournaments.run_interaction_game(actor, actor_starts=True)

if saved_actor_count > 0:   # if demo
    tournaments.run_topp_tournament(plot=True)
    win_rate = tournaments.run_one_vs_all(actor, display=False)
    print("Win rate for last actor:", win_rate)
    print("")
else:
    if config["size"] == 6:
        evaluation = tournaments.evaluate_actor(actor)
    else:
        evaluation = tournaments.run_one_vs_all(actor, 9)
    print("Evaluation:", evaluation)
    actor.save_model(config["name"])
    save_metadata(config, evaluation, time_spent)

    if config["size"] == 6 and evaluation > 0.5:
        elites = read_elites()
        elites[config["name"]] = evaluation
        save_elites(elites)
        print("Player was added to elites.")
    else:
        print("The player did not join the elites.")
