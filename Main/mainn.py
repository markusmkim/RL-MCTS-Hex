from time import time
from Main.config import config
from Tournaments.tournaments import Tournaments
from SimWorld.utils import visualize_game
from Main.utils import plot_histories, initialize_actor, initialize_critic, save_metadata, save_elites, read_elites, evaluate_progression
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
    plot_histories([evaluation_history], ["Evaluation"], config["save_frequency"])
    plot_histories([rph], ["Rollout prob"], config["save_frequency"])
    plot_histories([evaluation_history, rph], ["Evaluation", "Rollout prob"], config["save_frequency"])

if config["visualize_last_game"]:
    visualize_game(last_game_history)


print("Setting actor's epsilon to 0")
actor.epsilon = 0

if config["run_interaction_game"]:
    tournaments.run_interaction_game(actor, actor_starts=True)


evaluation = evaluate_progression(actor, saved_actor_count, tournaments, config["size"], final=True, plot_topp=True)

actor.save_model(config["name"])
save_metadata(config, evaluation, time_spent)

if config["size"] == 6 and evaluation > 0.5:
    elites = read_elites()
    elites[config["name"]] = evaluation
    save_elites(elites)
    print("Player was added to elites.")
else:
    print("The player did not join the elites.")
