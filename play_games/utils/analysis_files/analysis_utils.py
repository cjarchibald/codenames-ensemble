import matplotlib.pyplot as plt
import numpy as np
import json

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


class Stats: #ALL stats that will be used for graphing and for stat dict creation

    #KEYS FOR DATA GATHERING PHASE
    '''
    Keys for raw stats. These keys will be used for the stats gathered while parsing files. We can use the stats kepts under these keys to create 
    Statistics that mean something to us

    This first set of keys will be used to derive the average number of each type of word flipped per round. We will line them up with the number of rounds per
    game to calculate the average number of each word type flipped per game. 
    We can also calculate the average number of each type flipped per round by lining up with the number of guesses by round

    We can used the number of assassin words flipped to calculate the loss by assassin
    '''
    RED_WORDS_FLIPPED_BY_ROUND = "Red Words Flipped By Round"
    BLUE_WORDS_FLIPPED_BY_ROUND = "Blue Words Flipped By Round"
    BYSTANDER_WORDS_FLIPPED_BY_ROUND = "Bystander Words Flipped By Round"
    ASSASSIN_WORDS_FLIPPED_BY_ROUND = "Assassin Words Flipped By Round"

    """
    The next set of keys will represent data that can be used to help calculate the other stats. They can be used to divide stats by game, or round.
    They can also be used to calculate scores later. 

    Number of rounds per game:
    Will be stored as an array with each element as the number of rounds per game. This replaces game scores. 
    WE MUST LINE THIS UP WITH GAME WIN LOSS TO DERIVE THE GAME SCORES!!! If a number of rounds lines up with a loss, it's score is 25. If it lines up with a win,
    its score is the number of rounds

    Game win loss:
    array will be kept with 1s and 0s to represent the games won and lost respectively. Used to calculate Win Rate and can be paired with num rounds per
    game. See above description

    Clue Number by round:
    This can be used to gain insite into the relationship between clues given and words guessed

    """ 
    NUM_ROUNDS_PER_GAME = "Number of Rounds Per Game" 
    GAME_WIN_LOSS = "Game Win Loss" 
    CLUE_NUM_BY_ROUND = "Clue Number Given By Round"

    '''
    These are for learning experiments
    '''
    ARM_WEIGHTS_BY_ROUND = "Ensemble Arm Weights by Round"
    CHOSEN_BOTS_BY_ROUND = "Chosen Bots by Round"

    #KEYS FOR DATA PROCESSING (Use the keys for data gathering to access the saved dictionary and save data to a new dictionary)
    '''
    Note that as we process data we will do so on a game by game basis (like chunk processing) by getting the info for each game and appending the necessary
    values to the stats arrays. 
    Note that all of these stats are specific for a bot pairing over a certain number of games
    These stats are saved out for our visualizations
    '''

    '''
    These are the bread and butter stats that we do a lot of the work for. They will be used in the final dictionary. 
    The pair scores is an array that has the scores at the end of every round. We don't need to calculate a single value because the final value will be 
    at the end. These are created by creating a vector using the number of card types for each round and getting a prediction every time

    Pair scores has all of the pair scores at the end of every game so that we can take the average of each game accross all learning periods when doing our learning period analysis. 
    The final one is our average for the whole learning period/tournament. 
    '''
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


#These are the stat keys we use for graphing. They are the same as the bread and butter stats
MAIN_STATS_KEYS = [Stats.WIN_RATE, Stats.AVG_WIN_TIME, Stats.MIN_WIN_TIME, Stats.AVG_RED_FLIP_BY_GAME, Stats.AVG_BLUE_FLIP_BY_GAME, Stats.AVG_BYSTANDER_FLIP_BY_GAME, 
    Stats.AVG_ASSASSIN_FLIP_BY_GAME, Stats.FINAL_PAIR_SCORE]

PERFORMANCE_PROGRESSION_STATS = [Stats.PAIR_SCORES, Stats.RUNNING_AVG_WR, Stats.RUNNING_AVG_WT, Stats.RUNNING_AVG_RED_FLIP_BY_GAME, Stats.RUNNING_AVG_BLUE_FLIP_BY_GAME, Stats.RUNNING_AVG_BYSTANDER_FLIP_BY_GAME, Stats.RUNNING_AVG_ASSASSIN_FLIP_BY_GAME]
PERFORMANCE_PROGRESSION_SLIDING_WINDOW_STATS = [Stats.SLIDING_WINDOW_PAIR_SCORES, Stats.SLIDING_WINDOW_AVG_WR, Stats.SLIDING_WINDOW_AVG_WT, Stats.SLIDING_WINDOW_AVG_RED_FLIP_BY_GAME, Stats.SLIDING_WINDOW_AVG_BLUE_FLIP_BY_GAME, Stats.SLIDING_WINDOW_AVG_BYSTANDER_FLIP_BY_GAME, Stats.SLIDING_WINDOW_AVG_ASSASSIN_FLIP_BY_GAME]

#These are the keys that we will use to separate different kinds of stats in our overall StatDict. RECONSIDER THESE!!! TOO COMPLEX
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

class MinMaxKeys:
    MIN = "min"
    MAX = "max"

class DesiredStatsKeys:
    OPTIMAL_VALUE = "opimal value"
    OPTIMAL_EXTREME = "optimal extreme"

class DesiredStats():
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
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.xticks(rotation = -45, fontsize = 5)
    plt.savefig(save_file)
    plt.clf() 

def create_single_line_plot(x_axis, y_axis, label, title, x_label, y_label, save_file, has_best_fit):
    if has_best_fit:
        m, b = np.polyfit(x_axis, y_axis, 1)
        plt.plot(x_axis, m * x_axis + b)
    plt.plot(x_axis, y_axis, label = label)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.savefig(save_file)
    plt.clf()