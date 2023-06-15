import matplotlib.pyplot as plt
import numpy as np
import json
import os

#These are keys that are found in the round files so we can pick out the values that we want.
class RoundParseKeys:
    CODEMASTER = "CODEMASTER"
    GUESSER = "GUESSER"
    ROUND = "round"
    GUESS = "guess"
    GAME_LOST = "game lost"
    GAME_WON = "game won"
    CORRECT = "correct guess"
    BLUE = "incorrect guess"
    BYSTANDER = "bystander guessed"
    ASSASSIN = "assassin guessed"
    N_TARGETS = "num_targets"
    #These are used for starting a game at a certain state
    SEED = "seed"
    BOARD_WORDS = "board_words"
    RED_WORDS_LEFT = "red_words_left"
    BLUE_WORDS_LEFT = "blue_words_left"
    BYSTANDER_WORDS_LEFT = "bystander_words_left"
    ASSASSIN_WORD = "assassin_word"
    NUM_RED_WORDS_LEFT = "num_red_words_left"
    CLUE = "clue"
    TARGETS = "targets"
    GUESSES = "guesses"

class LearnParseKeys:
    START_TOKEN = "STARTING TO LEARN"
    CURR_TEAM_MATE_TOKEN = "guesser is"
    CHOSEN_BOT_TOKEN = 'chosen bot'
    BOT_WEIGHTS_TOKEN = 'bot weights:'
    END_TOKEN = 'end_status'

class CompiledDataKeys:
    STAT_COMPARISON = "Stat Comparison"
    ARM_WEIGHTS = "Arm Weights"
    PERCENTAGES = "Arm Percentages"
    PERF_PROG = "Performance Progression"
    PERF_PROG_SLIDE = "Performance Progression Sliding Window"
    FINAL_STAT_DIST = "Final Stat Distributions"


class Types:
    CM = 0
    G = 1


class Stats: #ALL stats that will be used for graphing and for stat dict creation

    #KEYS FOR DATA GATHERING PHASE
    RED_WORDS_FLIPPED_BY_ROUND = "Red Words Flipped By Round"
    BLUE_WORDS_FLIPPED_BY_ROUND = "Blue Words Flipped By Round"
    BYSTANDER_WORDS_FLIPPED_BY_ROUND = "Bystander Words Flipped By Round"
    ASSASSIN_WORDS_FLIPPED_BY_ROUND = "Assassin Words Flipped By Round"
    NUM_ROUNDS_PER_GAME = "Number of Rounds Per Game" 
    GAME_WIN_LOSS = "Game Win Loss" 
    CLUE_NUM_BY_ROUND = "Clue Number Given By Round"
    '''
    These are for learning experiments
    '''
    ARM_WEIGHTS_BY_ROUND = "Ensemble Arm Weights by Round"
    CHOSEN_BOTS_BY_ROUND = "Chosen Bots by Round"

    #KEYS FOR DATA PROCESSING (Use the keys for data gathering to access the saved dictionary and save data to a new dictionary)
    WIN_RATE = "Win Rate"
    AVG_WIN_TIME = "Average Win Time"
    MIN_WIN_TIME = "Min Win Time"
    PAIR_SCORES = "Bot Pairing Scores" #This can use different size vectors that are derived from the other stats. The final one is the average score. We want to keep all to make our cool graph
    FINAL_PAIR_SCORE = "Final Pair Score"
    AVG_RED_FLIP_BY_GAME = "Average Red Words Flipped By Game"
    AVG_BLUE_FLIP_BY_GAME = "Average Blue Words Flipped By Game"
    AVG_BYSTANDER_FLIP_BY_GAME = "Average Bystander Words Flipped By Game"
    AVG_ASSASSIN_FLIP_BY_GAME = "Average Assassin Words Flipped By Game"
    RED_FLIP_BY_GAME = "Red Words Flipped By Game"
    BLUE_FLIP_BY_GAME = "Blue Words Flipped By Game"
    BYSTANDER_FLIP_BY_GAME = "Bystander Words Flipped By Game"
    ASSASSIN_FLIP_BY_GAME = "Assassin Words Flipped By Game"
    PERCENTAGE_BOT_CHOSEN = "Percentage of Time Bots are Chosen"
    ARM_WEIGHTS_BY_GAME = "Ensemble Arm Weights by Game"

    RUNNING_AVG_WR = "Running Average Win Rate"
    RUNNING_AVG_WT = "Running Average Win Time"
    RUNNING_AVG_RED_FLIP_BY_GAME = "Running Average Red Words Flipped By Game"
    RUNNING_AVG_BLUE_FLIP_BY_GAME = "Running Average Blue Words Flipped By Game"
    RUNNING_AVG_BYSTANDER_FLIP_BY_GAME = "Running Average Bystander Words Flipped By Game"
    RUNNING_AVG_ASSASSIN_FLIP_BY_GAME = "Running Average Assassin Words Flipped By Game"

    SLIDING_WINDOW_PAIR_SCORES = "Sliding Window Average Pair Score"
    SLIDING_WINDOW_AVG_WR = "Sliding Window Average Win Rate"
    SLIDING_WINDOW_AVG_WT = "Sliding Window Average Win Time"
    SLIDING_WINDOW_AVG_RED_FLIP_BY_GAME = "Sliding Window Average Red Words Flipped By Game"
    SLIDING_WINDOW_AVG_BLUE_FLIP_BY_GAME = "Sliding Window Average Blue Words Flipped By Game"
    SLIDING_WINDOW_AVG_BYSTANDER_FLIP_BY_GAME = "Sliding Window Average Bystander Words Flipped By Game"
    SLIDING_WINDOW_AVG_ASSASSIN_FLIP_BY_GAME = "Sliding Window Average Assassin Words Flipped By Game"

    FINAL_STAT_DIST = "Final Stat Distribution"

class StatDictKeys: 
    G_LEARN_STATS = "Guesser Learning Stats"
    CM_LEARN_STATS = "Codemaster Learning Stats"
    FINAL_KEY = "Final"
    BEST_AVG = "Best Average"
    AVG_PERF = "Average Performance"
    BEST_OVERALL = "Best Overall"
    CODEMASTER = "Codemaster"
    GUESSER = "Guesser"
    SOLO_BOT_DATA = "Solo Bot Data"
    RANDOM = "Random"


COMPILED_DATA_STATS = [Stats.WIN_RATE, \
                            Stats.AVG_WIN_TIME, \
                            Stats.FINAL_PAIR_SCORE]

#These are the stat keys we use for graphing. They are the same as the bread and butter stats
MAIN_STATS_KEYS = [Stats.WIN_RATE, Stats.AVG_WIN_TIME, Stats.MIN_WIN_TIME, Stats.AVG_RED_FLIP_BY_GAME, Stats.AVG_BLUE_FLIP_BY_GAME, Stats.AVG_BYSTANDER_FLIP_BY_GAME, 
    Stats.AVG_ASSASSIN_FLIP_BY_GAME, Stats.FINAL_PAIR_SCORE]

PERFORMANCE_PROGRESSION_STATS = [Stats.PAIR_SCORES, Stats.RUNNING_AVG_WR, Stats.RUNNING_AVG_WT, Stats.RUNNING_AVG_RED_FLIP_BY_GAME, Stats.RUNNING_AVG_BLUE_FLIP_BY_GAME, Stats.RUNNING_AVG_BYSTANDER_FLIP_BY_GAME, Stats.RUNNING_AVG_ASSASSIN_FLIP_BY_GAME]
PERFORMANCE_PROGRESSION_SLIDING_WINDOW_STATS = [Stats.SLIDING_WINDOW_PAIR_SCORES, Stats.SLIDING_WINDOW_AVG_WR, Stats.SLIDING_WINDOW_AVG_WT, Stats.SLIDING_WINDOW_AVG_RED_FLIP_BY_GAME, Stats.SLIDING_WINDOW_AVG_BLUE_FLIP_BY_GAME, Stats.SLIDING_WINDOW_AVG_BYSTANDER_FLIP_BY_GAME, Stats.SLIDING_WINDOW_AVG_ASSASSIN_FLIP_BY_GAME]
FINAL_STAT_DIST_KEYS = MAIN_STATS_KEYS + [[StatDictKeys.CM_LEARN_STATS, Stats.PERCENTAGE_BOT_CHOSEN], [StatDictKeys.G_LEARN_STATS, Stats.PERCENTAGE_BOT_CHOSEN]]

#These are the keys that we will use to separate different kinds of stats in our overall StatDict. RECONSIDER THESE!!! TOO COMPLEX


class MinMaxKeys:
    MIN = "min"
    MAX = "max"

class DesiredStatsKeys:
    OPTIMAL_VALUE = "opimal value"
    OPTIMAL_EXTREME = "optimal extreme"

class DesiredStats:
    def __init__(self, stats, desired_stats_keys, min_max_keys):
        self.stats = stats
        self.desired_stats_keys = desired_stats_keys
        self.min_max_keys = min_max_keys
        self.set_desired_stats()
    
    def set_desired_stats(self):
        self.desired_stats = {
            self.stats.WIN_RATE : {
                self.desired_stats_keys.OPTIMAL_VALUE : 1.0,
                self.desired_stats_keys.OPTIMAL_EXTREME : self.min_max_keys.MAX
            },
            self.stats.AVG_WIN_TIME : {
                self.desired_stats_keys.OPTIMAL_VALUE : 0.0,
                self.desired_stats_keys.OPTIMAL_EXTREME : self.min_max_keys.MIN
            },
            self.stats.MIN_WIN_TIME : {
                self.desired_stats_keys.OPTIMAL_VALUE : 0.0,
                self.desired_stats_keys.OPTIMAL_EXTREME : self.min_max_keys.MIN
            }, 
            self.stats.AVG_RED_FLIP_BY_GAME: {
                self.desired_stats_keys.OPTIMAL_VALUE : 9.0,
                self.desired_stats_keys.OPTIMAL_EXTREME : self.min_max_keys.MAX
            }, 
            self.stats.AVG_BLUE_FLIP_BY_GAME : {
                self.desired_stats_keys.OPTIMAL_VALUE : 0.0,
                self.desired_stats_keys.OPTIMAL_EXTREME : self.min_max_keys.MIN
            }, 
            self.stats.AVG_BYSTANDER_FLIP_BY_GAME : {
                self.desired_stats_keys.OPTIMAL_VALUE : 0.0,
                self.desired_stats_keys.OPTIMAL_EXTREME : self.min_max_keys.MIN
            }, 
            self.stats.AVG_ASSASSIN_FLIP_BY_GAME : {
                self.desired_stats_keys.OPTIMAL_VALUE : 0.0,
                self.desired_stats_keys.OPTIMAL_EXTREME : self.min_max_keys.MIN
            }, 
            self.stats.FINAL_PAIR_SCORE : {
                self.desired_stats_keys.OPTIMAL_VALUE : np.inf,
                self.desired_stats_keys.OPTIMAL_EXTREME : self.min_max_keys.MAX
            }
        }
    
    def get_desired_stats(self, stat_key):
        return self.desired_stats[stat_key]

def load_dict(bests_json_path):
    best_team_mates = {}
    with open(bests_json_path) as f:
        best_team_mates = json.load(f)
    return best_team_mates

def create_path(fp):
    if not os.path.exists(os.path.dirname(fp)):
        os.makedirs(os.path.dirname(fp))

def save_json(json_obj, save_path):
    create_path(save_path)
    with open(save_path, 'w+') as f:
        json.dump(json_obj, f)

def load_json(filepath):
    with open(filepath, 'r') as f:
        json_obj = json.load(f)
    return json_obj

def graph_multiple_bar_chart(x_axis, y_axes, x_label, y_label, labels, title, save_path):
        width = .1
        ind = np.arange(len(x_axis))
        bars = []
        for i in range(len(y_axes)):
            bars.append(plt.bar(ind + (width * i), y_axes[i], width, label = labels[i]))

        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.xticks(ind+width, x_axis, rotation=-45)
        plt.title(title)
        plt.legend( tuple(bars), tuple(labels))
        plt.savefig(save_path)
        plt.clf() 

def graph_bar_chart(x_axis, y_axis, title, x_label, y_label, save_file):
    fig, ax = plt.subplots(layout="constrained")
    ax.bar(x_axis, y_axis)
    # plt.title(title)
    # plt.ylabel(y_label)
    # plt.xlabel(x_label)
    plt.xticks(rotation = -45, fontsize = 5)
    plt.savefig(save_file)
    plt.clf() 

def create_single_line_plot(x_axis, y_axis, label, title, x_label, y_label, save_file, has_best_fit):
    if has_best_fit:
        m, b = np.polyfit(x_axis, y_axis, 1)
        plt.plot(x_axis, m * x_axis + b)
    plt.plot(x_axis, y_axis, label = label)
    # plt.title(title)
    # plt.ylabel(y_label)
    # plt.xlabel(x_label)
    plt.savefig(save_file)
    plt.clf()

def extract_val(val):
    if isinstance(val, tuple) or isinstance(val, list):
        return val[0]
    return val

def find_ensemble(d):
    ensemble = None
    for bot in d:
        if ai_types.DISTANCE_ENSEMBLE == bot_ai_types.get_bot_ai_type(bot):
            ensemble = bot
            break  
    return ensemble

bot_ai_types = None 
ai_types = None

def set_globals(local_bot_ai_types, local_ai_types):
    global bot_ai_types
    global ai_types

    bot_ai_types = local_bot_ai_types
    ai_types = local_ai_types

def is_rand_ens(bot):
    if bot_ai_types.get_bot_ai_type(bot) == ai_types.RANDOM_DISTANCE_ENSEMBLE:
        return True 
    return False

def find_rand_bot(bots):
    #search through a list of bots and check their bot types. If they are rand, return it, otherwise return None 
    for bot in bots:
        if is_rand_ens(bot):
            return bot
    return

def check_if_ensemble(b):
    if ai_types.DISTANCE_ENSEMBLE == bot_ai_types.get_bot_ai_type(b):
        return True 
    return False