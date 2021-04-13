from time import time, sleep
from Main.config import config
from Tournaments.tournaments import Tournaments
from SimWorld.utils import visualize_game
from Main.utils import plot_history, initialize_actor, initialize_critic, train_actor
from Main.utils import save_metadata, save_kings, save_queens, read_kings, read_queens

# --- # --- # --- # --- # --- # --- # --- #
elite_group = "queens"
train_from = False
rollout_actor = False
plot_evaluation_history = True
visualize_last_game = False
run_interaction_game = False
# --- # --- # --- # --- # --- # --- # --- #

print("Welcome to a game of Hex!")

actor = initialize_actor(config, train_from)
critic = initialize_critic(config, train_from)

print("Actor initialized")

tournaments = Tournaments(config)
start_time = time()

evaluation_history, last_game_history, saved_actor_count = train_actor(actor, critic, config, tournaments, rollout_actor)

critic.save_model(config["name"])

time_spent = time() - start_time
print("Time spent on entire run:", time_spent)
print("")

if plot_evaluation_history and len(evaluation_history) > 0:
    plot_history(evaluation_history, config["save_frequency"])

if visualize_last_game:
    visualize_game(last_game_history)

print("Setting actor's epsilon to 0")
actor.epsilon = 0

if run_interaction_game:
    tournaments.run_interaction_game(actor, actor_starts=True)

if saved_actor_count > 0:
    win_rate = tournaments.run_one_vs_all(actor)
    print("Win rate for last actor:", win_rate)
    print("")
    tournaments.run_topp_tournament(plot=True)
else:
    if config["size"] == 6:
        evaluation = tournaments.evaluate_actor(actor)
    else:
        evaluation = tournaments.run_one_vs_all(actor, 9)
    print("Evaluation:", evaluation)
    actor.save_model(config["name"])
    save_metadata(config, evaluation, time_spent)

    if config["size"] == 6 and evaluation > 0.5:
        if elite_group == "queens":
            queens = read_queens()
            queens[config["name"]] = evaluation
            save_queens(queens)
            print("Player was added to queens.")

        if elite_group == "kings":
            kings = read_kings()
            kings[config["name"]] = evaluation
            save_kings(kings)
            print("Player was added to kings.")
    else:
        print("The player did not join the elites.")
