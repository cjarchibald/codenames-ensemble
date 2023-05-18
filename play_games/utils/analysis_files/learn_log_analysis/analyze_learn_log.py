from statistics import mean, median
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches
import numpy as np
import sys


from stats.stat_utils import BestsKeys, create_alternate_dict, STAT_KEYS
from stats.parsers.table_parser import parse_file
from stats.parsers.round_log_parser import all_vecs_parse
import utils.analyze_learn_log_utils as analyze_learn_log_utils
from utils.analyze_learn_log_utils import graph_multiple_bar_chart, \
    analyze_learn_logs_stats_path, graph_bar_chart, create_single_line_plot, load_dict
from run_games_spencer.utils.experiment_settings import INCLUDE_SAME_LM


class LearnLogAnalyzer:
    def __init__(self, utils):
        self.utils = utils

plot_directory = project_root_path + 'logs/learning_plots/'
stat_path = project_root_path + 'stats/'

START_TOKEN = analyze_learn_log_utils.START_TOKEN
CURR_TEAM_MATE_TOKEN = analyze_learn_log_utils.CURR_TEAM_MATE_TOKEN
CHOSEN_BOT_TOKEN = analyze_learn_log_utils.CHOSEN_BOT_TOKEN
BOT_WEIGHTS_TOKEN = analyze_learn_log_utils.BOT_WEIGHTS_TOKEN
END_TOKEN = analyze_learn_log_utils.END_TOKEN
GAME_ACCURACY_TOKEN = analyze_learn_log_utils.GAME_ACCURACY_TOKEN
WIN_RATE_TOKEN = analyze_learn_log_utils.WIN_RATE_TOKEN
PREDICTED_BOT_TOKEN = analyze_learn_log_utils.PREDICTED_BOT_TOKEN

CHOSEN_BOT_KEY = analyze_learn_log_utils.CHOSEN_BOT_KEY
BOT_WEIGHTS_KEY = analyze_learn_log_utils.BOT_WEIGHTS_KEY
GAME_ACCURACY_KEY = analyze_learn_log_utils.GAME_ACCURACY_KEY
WIN_RATE_KEY = analyze_learn_log_utils.WIN_RATE_KEY
PREDICTED_BOTS_KEY = analyze_learn_log_utils.PREDICTED_BOTS_KEY
GAMES_WON_KEY = analyze_learn_log_utils.GAMES_WON_KEY
TIMES_CHOSEN_KEY = analyze_learn_log_utils.TIMES_CHOSEN_KEY

CORRECT_TIMES_CHOSEN_KEY = analyze_learn_log_utils.CORRECT_TIMES_CHOSEN_KEY


files = []

def get_values(f):
    line = f.readline()
    line = line.strip()
    values = line.split(": ")
    return values

def parse_learn_log(fp):
    stat_dict = {}
    with open(fp, 'r') as f:
        learning_period_team_mate = ''
        for line in f:
            line = line.strip()
            values = line.split(": ")
            if values[0] == START_TOKEN:
                values = get_values(f)
                learning_period_team_mate = values[1]
                stat_dict[learning_period_team_mate] = {}
            elif values[0] == CHOSEN_BOT_TOKEN:
                if CHOSEN_BOT_KEY not in stat_dict[learning_period_team_mate].keys():
                    stat_dict[learning_period_team_mate][CHOSEN_BOT_KEY] = []
                stat_dict[learning_period_team_mate][CHOSEN_BOT_KEY].append(values[1])
            elif values[0] == BOT_WEIGHTS_TOKEN:
                values = get_values(f)
                while values[0] != '':
                    #At this point, we know that we are in a learning period
                    if BOT_WEIGHTS_KEY not in stat_dict[learning_period_team_mate].keys():
                        stat_dict[learning_period_team_mate][BOT_WEIGHTS_KEY] = {}
                    #Create a list of the bot weights for each bot type in the ensamble for every round
                    if values[0] not in stat_dict[learning_period_team_mate][BOT_WEIGHTS_KEY].keys():
                        stat_dict[learning_period_team_mate][BOT_WEIGHTS_KEY][values[0]] = []
                    stat_dict[learning_period_team_mate][BOT_WEIGHTS_KEY][values[0]].append(float(values[1]))
                    values = get_values(f)
            elif values[0] == GAME_ACCURACY_TOKEN:
                if GAME_ACCURACY_KEY not in stat_dict[learning_period_team_mate].keys():
                    stat_dict[learning_period_team_mate][GAME_ACCURACY_KEY] = []
                stat_dict[learning_period_team_mate][GAME_ACCURACY_KEY].append(float(values[1]))
            elif values[0] == WIN_RATE_TOKEN:
                if WIN_RATE_KEY not in stat_dict[learning_period_team_mate].keys():
                    stat_dict[learning_period_team_mate][WIN_RATE_KEY] = []
                stat_dict[learning_period_team_mate][WIN_RATE_KEY].append(float(values[1]))
            elif values[0] == PREDICTED_BOT_TOKEN:
                if PREDICTED_BOTS_KEY not in stat_dict[learning_period_team_mate].keys():
                    stat_dict[learning_period_team_mate][PREDICTED_BOTS_KEY] = []
                stat_dict[learning_period_team_mate][PREDICTED_BOTS_KEY].append(values[1])
            elif values[0] == END_TOKEN:
                if GAMES_WON_KEY not in stat_dict[learning_period_team_mate].keys():
                    stat_dict[learning_period_team_mate][GAMES_WON_KEY] = []
                if values[1] == 'win':
                    stat_dict[learning_period_team_mate][GAMES_WON_KEY].append(1)
                else:
                    stat_dict[learning_period_team_mate][GAMES_WON_KEY].append(0)

    return stat_dict

def create_chosen_bot_chart(stat_dict):
    results = {}
    stats = list(best_team_mates[list(best_team_mates.keys())[0]].keys())
    team_mates = stat_dict.keys()
    for stat in stats:
        x_axis = []
        y_axis = []
        for key in team_mates:
            if key not in results.keys():
                results[key] = {}
                results[key][CORRECT_TIMES_CHOSEN_KEY] = {}
            results[key][CORRECT_TIMES_CHOSEN_KEY][stat] = 0
            x_axis.append(key)
            chosen_bots = stat_dict[key][CHOSEN_BOT_KEY]
            total_bots_chosen = len(chosen_bots)
            match = best_team_mates[key][stat][BestsKeys.BOTS_KEY]
            for bot in chosen_bots:
                if bot in match:
                    results[key][CORRECT_TIMES_CHOSEN_KEY][stat] += 1
            percent_correct = results[key][CORRECT_TIMES_CHOSEN_KEY][stat] / total_bots_chosen
            y_axis.append(percent_correct)

        title = "Percentage of correct bots chosen per round for " + stat
        x_label = "team mate"
        y_label = "percentage"
        save_file = plot_directory + stat.replace(" ", "_").lower() + '_chosen_bot_chart.png'
        files.append(save_file)

        graph_bar_chart(x_axis, y_axis, title, x_label, y_label, save_file)
    
    return results

def plot_win_rates(stat_dict):

    for key in stat_dict.keys():
        label = key
        title = "win rate with " + key
        x_label = 'game'
        y_label = 'percent'
        save_file = plot_directory + 'win_rate_' + key.replace(" ", "_") + '_chart.png'
        files.append(save_file)
        win_rates = np.array(stat_dict[key][WIN_RATE_KEY])
        x_axis = np.array(list(range(1, len(win_rates) + 1)))
        has_best_fit = True

        create_single_line_plot(x_axis, win_rates, label, title, x_label, y_label, save_file, has_best_fit)


def plot_games_won(stat_dict):
    for key in stat_dict.keys():
        win_log = stat_dict[key][GAMES_WON_KEY]
        x_axis = list(range(1, len(win_log) + 1))
        curr_total = 0
        y_axis = []
        for num in win_log:
            curr_total += num
            y_axis.append(curr_total / len(x_axis))
        
        save_file = plot_directory + 'games_won_' + key.replace(" ", "_") + '_chart.png'
        files.append(save_file)
        title = "percent of total games won with " + key
        x_label = "game"
        y_label = "percent"

        create_single_line_plot(x_axis, y_axis, key, title, x_label, y_label, save_file, False)

def plot_game_accuracy(stat_dict):
    for key in stat_dict.keys():
        game_accuracies = np.array(stat_dict[key][GAME_ACCURACY_KEY])
        x_axis = np.array(list(range(1, len(game_accuracies) + 1)))
        save_file = plot_directory + 'game_accuracy_' + key.replace(" ", "_") + 'chart.png'
        files.append(save_file)
        title = "game accuracy with " + key
        x_label = "game"
        y_label = "percent"

        create_single_line_plot(x_axis, game_accuracies, key, title, x_label, y_label, save_file, True)

def plot_scores(stat_dict):
    for key in stat_dict.keys():
        for bot_key in stat_dict[key][BOT_WEIGHTS_KEY].keys():
            bot_weights = stat_dict[key][BOT_WEIGHTS_KEY][bot_key]
            x_axis = list(range(1, len(bot_weights) + 1))
            plt.plot(x_axis, bot_weights, label = bot_key)
        plt.legend()
        plt.title("bot weights with "  + key)
        plt.ylabel('score')
        plt.xlabel('round')
        save_file = plot_directory + 'bot_weight_' + key.replace(" ", "_") + 'chart.png'
        files.append(save_file)
        plt.savefig(save_file)
        plt.clf()

def do_other_calculations(results, stat_dict):
    
    for team_mate in stat_dict.keys():
        results[team_mate][TIMES_CHOSEN_KEY] = {}
        chosen_bots = stat_dict[team_mate][CHOSEN_BOT_KEY]
        for bot in chosen_bots:
            if bot not in results[team_mate][TIMES_CHOSEN_KEY].keys():
                results[team_mate][TIMES_CHOSEN_KEY][bot] = 0
            results[team_mate][TIMES_CHOSEN_KEY][bot] += 1

    return results

def graph_lp_scores(stat_dict, path, path2):
    x_axis = []
    y_axis_min = []
    y_axis_max = []
    y_axis_mean = []
    y_axis_median = []
    y_axis_single = []
    for team_mate in stat_dict.keys():
        x_axis.append(team_mate)
        y_axis_min.append(min(stat_dict[team_mate][GAME_ACCURACY_KEY]))
        y_axis_mean.append(mean(stat_dict[team_mate][GAME_ACCURACY_KEY]))
        y_axis_median.append(median(stat_dict[team_mate][GAME_ACCURACY_KEY]))
        y_axis_max.append(max(stat_dict[team_mate][GAME_ACCURACY_KEY]))
        #The final value in the win rate array is the ending winrate for the whole learning period
        y_axis_single.append(stat_dict[team_mate][WIN_RATE_KEY][-1])

    graph_multiple_bar_chart(x_axis, [y_axis_mean, y_axis_median, y_axis_min, y_axis_max], "Team Mate", "Score", \
        ["mean", 'median', 'min', 'max'], f"Scores accross learning period for {GAME_ACCURACY_KEY}", path)
    graph_bar_chart(x_axis, y_axis_single, f"Scores accross learning period for {WIN_RATE_KEY}", "Team Mate", "Score", path2)

def graph_bot_perc(stat_dict, path_base):
    paths = []
    for team_mate in stat_dict.keys():
        path = path_base + team_mate.replace(" ", "_") + ".png"
        paths.append(path)
        x_axis = []
        y_axis = []
        chosen_bots = stat_dict[team_mate][CHOSEN_BOT_KEY]
        bot_counts = {}
        for bot in chosen_bots:
            if bot not in bot_counts.keys():
                bot_counts[bot] = 0
            bot_counts[bot] += 1
        for bot in bot_counts.keys():
            x_axis.append(bot)
            percentage = bot_counts[bot] / len(stat_dict[team_mate][CHOSEN_BOT_KEY])
            y_axis.append(percentage)
        
        graph_bar_chart(x_axis, y_axis, f"Percentage of bots selected for\n{team_mate}", "Team Mate", "Percentage", path)
    return paths

def save_data(save_path, stat_dict):
    doc = Document()

    path = analyze_learn_logs_stats_path + "single_learn_log_" + GAME_ACCURACY_KEY.replace(" ", "_").lower() + ".png"
    path2 = analyze_learn_logs_stats_path + "single_learn_log_" + WIN_RATE_KEY.replace(" ", "_").lower() + ".png"
    files.extend([path, path2])

    graph_lp_scores(stat_dict, path, path2) 
    
    path_base = analyze_learn_logs_stats_path + "bot_percentages-"
    files.extend(graph_bot_perc(stat_dict, path_base))

    for filepath in files:
        doc.add_picture(filepath, width=Inches(5), height=Inches(4))

    doc.save(save_path)

def parse_table(table_fp):
    game_dictionary = parse_file(table_fp)
    table_dictionary = create_alternate_dict(game_dictionary, STAT_KEYS, INCLUDE_SAME_LM)
    return table_dictionary

def parse_logs(learn_log_fp, table_fp, round_log_fp):
    learn_log_stat_dict = parse_learn_log(learn_log_fp)
    table_stat_dict = parse_table(table_fp)
    round_log_stat_dict = all_vecs_parse(round_log_fp)
    return learn_log_stat_dict, table_stat_dict, round_log_stat_dict

def analyze_learn_log(learn_log_filepath, table_filepath, round_log_filepath, save_path, bests):
    global best_team_mates
    if bests == None:
        best_team_mates = load_dict()
    else:
        best_team_mates = bests

    files.clear()

    learn_log_stat_dict, table_stat_dict, round_log_stat_dict = parse_logs(learn_log_filepath, table_filepath, round_log_filepath)
    plot_scores(learn_log_stat_dict)
    learn_log_results = create_chosen_bot_chart(learn_log_stat_dict)
    plot_win_rates(learn_log_stat_dict)
    plot_games_won(learn_log_stat_dict)
    plot_game_accuracy(learn_log_stat_dict)
    do_other_calculations(learn_log_results, learn_log_stat_dict)
    save_data(save_path, learn_log_stat_dict)
    return learn_log_stat_dict, table_stat_dict, learn_log_results, round_log_stat_dict

if __name__=="__main__":
    source_root = '/Users/spencerbrosnahan/Documents/GitHub/codenames-ai/logs/'
    save_root = '/Users/spencerbrosnahan/Documents/Research/Experiment-Results/learning_stats/'
    analyze_learn_log(source_root + "learn_log_T1_WO_S_PR_L_0_CM.txt", source_root + "parsable_table_stats_T1_WO_S_PR_L_0.txt", source_root + "round_log_T1_WO_S_PR_L_0.txt", save_root + "cm_learning_tables_T1_WO_S_PR_L_0.docx", None)