import json
import numpy as np
import joblib
from tabulate import tabulate
import copy
import matplotlib.pyplot as plt
import os
import scipy.stats as stats
from matplotlib.ticker import MaxNLocator

class types:
    CM = 0
    G = 1

'''
This class is responsible for the stats analysis flow

parse data -> save to file -> process data -> save to file -> visual
'''
class ResultsAnalyzer:
    def __init__(self, experiment_settings, file_paths_obj, round_log_parser, learn_log_parser, stats, stat_dict_keys, \
        experiment_types, bot_ai_types, ai_types, main_stats_keys, performance_progression_stat_keys, performance_progression_sliding_window_stat_keys, desired_stats, desired_stats_keys, min_max_keys, 
        lm_types, bot_lm_types):
        self.experiment_settings = experiment_settings
        self.file_paths_obj = file_paths_obj
        self.round_log_parser = round_log_parser
        self.learn_log_parser = learn_log_parser
        self.stats = stats
        self.stat_dict_keys = stat_dict_keys
        self.experiment_types = experiment_types
        self.bot_ai_types = bot_ai_types
        self.ai_types = ai_types
        self.main_stats_keys = main_stats_keys
        self.performance_progression_stat_keys = performance_progression_stat_keys
        self.performance_progression_sliding_window_stat_keys = performance_progression_sliding_window_stat_keys
        self.desired_stats = desired_stats
        self.desired_stats_keys = desired_stats_keys
        self.min_max_keys = min_max_keys
        self.lm_types = lm_types
        self.bot_lm_types = bot_lm_types
        self.precision = 4
        self.confidence_level = .95
        self.use_preloaded_parsed = False
        self.use_preloaded_processed = False
        self.use_preloaded_visualized = False

        self.conversion = {
            self.stats.PAIR_SCORES: self.stats.FINAL_PAIR_SCORE,
            self.stats.RUNNING_AVG_WR: self.stats.WIN_RATE, 
            self.stats.RUNNING_AVG_WT: self.stats.AVG_WIN_TIME, 
            self.stats.RUNNING_AVG_RED_FLIP_BY_GAME: self.stats.AVG_RED_FLIP_BY_GAME,
            self.stats.RUNNING_AVG_BLUE_FLIP_BY_GAME: self.stats.AVG_BLUE_FLIP_BY_GAME,
            self.stats.RUNNING_AVG_BYSTANDER_FLIP_BY_GAME: self.stats.AVG_BYSTANDER_FLIP_BY_GAME,
            self.stats.RUNNING_AVG_ASSASSIN_FLIP_BY_GAME: self.stats.AVG_ASSASSIN_FLIP_BY_GAME, 

            self.stats.SLIDING_WINDOW_PAIR_SCORES: self.stats.FINAL_PAIR_SCORE,
            self.stats.SLIDING_WINDOW_AVG_WR: self.stats.WIN_RATE, 
            self.stats.SLIDING_WINDOW_AVG_WT: self.stats.AVG_WIN_TIME, 
            self.stats.SLIDING_WINDOW_AVG_RED_FLIP_BY_GAME: self.stats.AVG_RED_FLIP_BY_GAME,
            self.stats.SLIDING_WINDOW_AVG_BLUE_FLIP_BY_GAME: self.stats.AVG_BLUE_FLIP_BY_GAME,
            self.stats.SLIDING_WINDOW_AVG_BYSTANDER_FLIP_BY_GAME: self.stats.AVG_BYSTANDER_FLIP_BY_GAME,
            self.stats.SLIDING_WINDOW_AVG_ASSASSIN_FLIP_BY_GAME: self.stats.AVG_ASSASSIN_FLIP_BY_GAME
        }
        plt.rcParams['figure.figsize'] = [10, 8]
        plt.rcParams['figure.subplot.bottom'] = 0.15
    
    def parse_data(self, round_logs, learn_logs_cm, learn_logs_g, parsed_data_filepaths):

        #Compile the needed filepaths to parse

        #All experiments parse the round logs
        parsed_round_log_data = self.round_log_parser.run_parser(round_logs)

        #If it is a learning experiment, then we need to parse the learn logs as well
        if len(learn_logs_cm) != 0:
            parsed_learn_log_data_cm = self.learn_log_parser.run_parser(learn_logs_cm)
        if len(learn_logs_g) != 0:
            parsed_learn_log_data_g = self.learn_log_parser.run_parser(learn_logs_g)

        #Save the data
        final_dict = {}
        for counter, filepath in enumerate(parsed_data_filepaths):
            try:
                merged_dict = parsed_round_log_data[counter]
                if len(learn_logs_cm) != 0:
                    llcm_dict = parsed_learn_log_data_cm[counter]
                    self.merge_data(merged_dict, llcm_dict, types.CM)
                if len(learn_logs_g) != 0:
                    llg_dict = parsed_learn_log_data_g[counter]
                    self.merge_data(merged_dict, llg_dict, types.G)

                final_dict[counter] = merged_dict

                with open(filepath, 'w+') as f:
                    json.dump(merged_dict, f)

            except:
                continue

        return final_dict

    def process_data(self, parsed_data, processed_data_filepaths):
        processed_data = {}

        #Load up the parsed data if needed
        if parsed_data == None:
            parsed_data = self.load_parsed_data()
        
        #I need a dictionary for holding all of the data across learn periods

        #At this point, we know that our data is parsed and loaded into the corred class variables 

        #Do the round log specific processing
        #win rate, avg win time, min win time, pair scores, avg red, blue, bys, assas flipped by game
        
        #loop through lps, cms, and gs and then calculate all of the scores
        for lp in parsed_data:
            processed_data[lp] = {}
            for cm in parsed_data[lp]:
                processed_data[lp][cm] = {}
                for g in parsed_data[lp][cm]:
                    processed_data[lp][cm][g] = {}
                    #For each learning period and for each pairing, calculate stats
                    data = parsed_data[lp][cm][g]

                    # if self.experiment_settings.experiment_type == None:
                    #     entry = self.get_mean_w_moe(data[self.stats.GAME_WIN_LOSS])
                    # else:
                    #     entry = np.average(data[self.stats.GAME_WIN_LOSS])

                    #calculate lp win rate
                    processed_data[lp][cm][g][self.stats.WIN_RATE] = np.average(data[self.stats.GAME_WIN_LOSS])

                    #calculate lp avg win time
                    win_times = self.get_win_times(data[self.stats.GAME_WIN_LOSS], data[self.stats.NUM_ROUNDS_PER_GAME])


                    # if self.experiment_settings.experiment_type == None:
                    #     entry = self.get_mean_w_moe(win_times)
                    # else:
                    #     entry = np.average(win_times)


                    if len(win_times) != 0: processed_data[lp][cm][g][self.stats.AVG_WIN_TIME] = np.average(win_times)
                    else: processed_data[lp][cm][g][self.stats.AVG_WIN_TIME] = 25.0

                    #calculate lp min win time
                    if len(win_times) != 0: processed_data[lp][cm][g][self.stats.MIN_WIN_TIME] = min(win_times)
                    else: processed_data[lp][cm][g][self.stats.MIN_WIN_TIME] = 25.0

                    #calculate lp pair scores (at the end of every game)
                    processed_data[lp][cm][g][self.stats.PAIR_SCORES] = self.get_pair_scores(data[self.stats.NUM_ROUNDS_PER_GAME], \
                        data[self.stats.RED_WORDS_FLIPPED_BY_ROUND], data[self.stats.BLUE_WORDS_FLIPPED_BY_ROUND], \
                        data[self.stats.BYSTANDER_WORDS_FLIPPED_BY_ROUND], data[self.stats.ASSASSIN_WORDS_FLIPPED_BY_ROUND])
                    
                    processed_data[lp][cm][g][self.stats.FINAL_PAIR_SCORE] = processed_data[lp][cm][g][self.stats.PAIR_SCORES][-1]

                    #calculate lp avg red words flipped per game
                    flips = self.calculate_flips_by_game(parsed_data, self.stats.RED_WORDS_FLIPPED_BY_ROUND, lp, cm, g)
                    processed_data[lp][cm][g][self.stats.RED_FLIP_BY_GAME] = flips
                    processed_data[lp][cm][g][self.stats.AVG_RED_FLIP_BY_GAME] = np.average(flips)

                    #calculate lp avg blue words flipped per game
                    flips = self.calculate_flips_by_game(parsed_data, self.stats.BLUE_WORDS_FLIPPED_BY_ROUND, lp, cm, g)
                    processed_data[lp][cm][g][self.stats.BLUE_FLIP_BY_GAME] = flips
                    processed_data[lp][cm][g][self.stats.AVG_BLUE_FLIP_BY_GAME] = np.average(flips)

                    #calculate lp avg bystander words flipped per game
                    flips = self.calculate_flips_by_game(parsed_data, self.stats.BYSTANDER_WORDS_FLIPPED_BY_ROUND, lp, cm, g)
                    processed_data[lp][cm][g][self.stats.BYSTANDER_FLIP_BY_GAME] = flips
                    processed_data[lp][cm][g][self.stats.AVG_BYSTANDER_FLIP_BY_GAME] = np.average(flips)

                    #calculate lp avg assassin words flipped per game
                    flips = self.calculate_flips_by_game(parsed_data, self.stats.ASSASSIN_WORDS_FLIPPED_BY_ROUND, lp, cm, g)
                    processed_data[lp][cm][g][self.stats.ASSASSIN_FLIP_BY_GAME] = flips
                    processed_data[lp][cm][g][self.stats.AVG_ASSASSIN_FLIP_BY_GAME] = np.average(flips)

                    #calculate cm or g learn stats if it is a learning experiment with either an ensemble cm or g
                    if len(self.file_paths_obj.learn_log_filepaths_cm) > 0:
                        self.process_learning_data(processed_data, parsed_data, lp, cm, g, self.stat_dict_keys.CM_LEARN_STATS)
                    if len(self.file_paths_obj.learn_log_filepaths_g) > 0:
                        self.process_learning_data(processed_data, parsed_data, lp, cm, g, self.stat_dict_keys.G_LEARN_STATS)
                    
                    self.get_running_averages(processed_data, parsed_data, lp, cm, g)
                    self.get_sliding_window_averages(processed_data, parsed_data, lp, cm, g)

        #If it is a learning experiment, we want to take averages across lps for stats and we store them in another file
        if self.experiment_settings.experiment_type == self.experiment_types.LEARNING_EXPERIMENT or self.experiment_settings.experiment_type == self.experiment_types.PARAMETER_EXPERIMENT:
            processed_data[self.stat_dict_keys.FINAL_KEY] = self.get_averages(processed_data)

            #Save the final data structure
            with open(processed_data_filepaths[-1], 'w+') as f:
                json.dump(processed_data[self.stat_dict_keys.FINAL_KEY], f)
            
            end = -1
        else:
            end = len(processed_data_filepaths)

        #save the data for individual files
        for counter in parsed_data.keys():
            filepath = processed_data_filepaths[counter]
            with open(filepath, 'w+') as f:
                json.dump(processed_data[counter], f)

        return processed_data
    
    def calc_bot_score_sliding_window(self, data):
        sliding_wind_avgs = []

        event_arrays = self.get_event_arrays(data[self.stats.NUM_ROUNDS_PER_GAME], \
                        data[self.stats.RED_WORDS_FLIPPED_BY_ROUND], data[self.stats.BLUE_WORDS_FLIPPED_BY_ROUND], \
                        data[self.stats.BYSTANDER_WORDS_FLIPPED_BY_ROUND], data[self.stats.ASSASSIN_WORDS_FLIPPED_BY_ROUND])
        #TODO: Finish calculating this

        #Generate all of the events that are possible
        pos_events = self.generate_pos_events()

        #load the model
        model = joblib.load(self.file_paths_obj.model_path)

        for i in range(len(event_arrays)):
            #A dictionary that keeps thrack of all the events we've seen up until now
            events = {}

            #Put those counts in a dictionary
            for e in pos_events:
                events[e] = 0

            for g in event_arrays[i:]:
                for round_outcome in g:
                    e = self.create_string(round_outcome)
                    events[e] += 1

            vec = self.get_feature_vec(events, pos_events)
            sliding_wind_avgs.append(model.predict(np.array(vec).reshape(1, -1))[0])
        
        return sliding_wind_avgs

    
    def calc_sliding_window_averages(self, data):
        sliding_wind_avgs = []
        for i in range(len(data)):
            sliding_wind_avgs.append(np.mean(data[i:]))
        return sliding_wind_avgs
    
    def calc_sliding_window_average_wt(self, data):
        sliding_wind_avgs = []
        # at any values of zero, I just need to put whatever the mean is 
        for i in range(len(data)):
            curr_window = self.calc_run_avg_wt(data[i:])
            if len(curr_window) > 0:
                sliding_wind_avgs.append(curr_window[-1])
            else:
                sliding_wind_avgs.append(sliding_wind_avgs[-1])
        return sliding_wind_avgs


    def get_sliding_window_averages(self, processed_data, parsed_data, lp, cm, g):
        processed_data[lp][cm][g][self.stats.SLIDING_WINDOW_PAIR_SCORES] = self.calc_bot_score_sliding_window(parsed_data[lp][cm][g])
        processed_data[lp][cm][g][self.stats.SLIDING_WINDOW_AVG_WR] = self.calc_sliding_window_averages(parsed_data[lp][cm][g][self.stats.GAME_WIN_LOSS])
        arr = [parsed_data[lp][cm][g][self.stats.NUM_ROUNDS_PER_GAME][i] if parsed_data[lp][cm][g][self.stats.GAME_WIN_LOSS][i] == 1 else 0 for i in range(len(parsed_data[lp][cm][g][self.stats.NUM_ROUNDS_PER_GAME]))]
        processed_data[lp][cm][g][self.stats.SLIDING_WINDOW_AVG_WT] = self.calc_sliding_window_average_wt(arr)
        processed_data[lp][cm][g][self.stats.SLIDING_WINDOW_AVG_RED_FLIP_BY_GAME] = self.calc_sliding_window_averages(processed_data[lp][cm][g][self.stats.RED_FLIP_BY_GAME])
        processed_data[lp][cm][g][self.stats.SLIDING_WINDOW_AVG_BLUE_FLIP_BY_GAME] = self.calc_sliding_window_averages(processed_data[lp][cm][g][self.stats.BLUE_FLIP_BY_GAME])
        processed_data[lp][cm][g][self.stats.SLIDING_WINDOW_AVG_BYSTANDER_FLIP_BY_GAME] = self.calc_sliding_window_averages(processed_data[lp][cm][g][self.stats.BYSTANDER_FLIP_BY_GAME])
        processed_data[lp][cm][g][self.stats.SLIDING_WINDOW_AVG_ASSASSIN_FLIP_BY_GAME] = self.calc_sliding_window_averages(processed_data[lp][cm][g][self.stats.ASSASSIN_FLIP_BY_GAME])


    def get_running_averages(self, processed_data, parsed_data, lp, cm, g):
        # self.stats, self.stat_dict_keys
        processed_data[lp][cm][g][self.stats.RUNNING_AVG_WR] = self.calc_run_avg(parsed_data[lp][cm][g][self.stats.GAME_WIN_LOSS])
        arr = [parsed_data[lp][cm][g][self.stats.NUM_ROUNDS_PER_GAME][i] if parsed_data[lp][cm][g][self.stats.GAME_WIN_LOSS][i] == 1 else 0 for i in range(len(parsed_data[lp][cm][g][self.stats.NUM_ROUNDS_PER_GAME]))]
        processed_data[lp][cm][g][self.stats.RUNNING_AVG_WT] = self.calc_run_avg_wt(arr)
        processed_data[lp][cm][g][self.stats.RUNNING_AVG_RED_FLIP_BY_GAME] = self.calc_run_avg(processed_data[lp][cm][g][self.stats.RED_FLIP_BY_GAME])
        processed_data[lp][cm][g][self.stats.RUNNING_AVG_BLUE_FLIP_BY_GAME] = self.calc_run_avg(processed_data[lp][cm][g][self.stats.BLUE_FLIP_BY_GAME])
        processed_data[lp][cm][g][self.stats.RUNNING_AVG_BYSTANDER_FLIP_BY_GAME] = self.calc_run_avg(processed_data[lp][cm][g][self.stats.BYSTANDER_FLIP_BY_GAME])
        processed_data[lp][cm][g][self.stats.RUNNING_AVG_ASSASSIN_FLIP_BY_GAME] = self.calc_run_avg(processed_data[lp][cm][g][self.stats.ASSASSIN_FLIP_BY_GAME])

    def calc_run_avg_wt(self, arr):
        running_averages = []
        curr_sum = 0
        curr_count = 0
        for e in arr:
            if e == 0:
                if len(running_averages) > 0:
                    running_averages.append(running_averages[-1])
                else:
                    running_averages.append(0)
                continue #we don't count it
            curr_sum += e
            curr_count += 1
            running_averages.append(curr_sum / curr_count)
        return running_averages
    
    def calc_run_avg(self, arr):
        curr_sum = 0
        curr_count = 0
        new_arr = []
        for e in arr:
            curr_sum += e 
            curr_count += 1 
            new_arr.append(curr_sum / curr_count)
        return new_arr

    def visualize_data(self, processed_data=None):
        #This is where we create the figures using our processed data

        if processed_data is None:
            processed_data = self.load_processed_data()

        #This is the function that creates the basic tournament cross-table
        #loop through all lps if you want, need to add loop though. I currently just use the final one 

        # self.create_main_table(processed_data[self.stat_dict_keys.FINAL_KEY], self.file_paths_obj.tournament_table_filepaths[-1])

        #Check if this is a learning experiment
        if self.experiment_settings.experiment_type == self.experiment_types.LEARNING_EXPERIMENT:
            #TODO: loop through all of the lps here
            lp = -1
            performance_stats = self.create_learn_table(processed_data[self.stat_dict_keys.FINAL_KEY], self.file_paths_obj.learn_table_filepaths[lp])
            self.create_performance_progression_figures(processed_data[self.stat_dict_keys.FINAL_KEY], lp, performance_stats)
            self.create_performance_progression_sliding_window_figures(processed_data[self.stat_dict_keys.FINAL_KEY], lp, performance_stats)
            self.create_arm_percentage_figures(processed_data[self.stat_dict_keys.FINAL_KEY], lp)
            self.create_arm_weights_figures(processed_data[self.stat_dict_keys.FINAL_KEY], lp)
        elif self.experiment_settings.experiment_type == self.experiment_types.PARAMETER_EXPERIMENT:
            self.create_param_vs_score_figures(processed_data)

    def compile_data(self):
        #This is where we compile all of the figures and tables into a file 

        #Create one pdf page per pairing (one for W and WO as well). Get the table data as well and place it on page
        pass

    def run_analysis(self):
        
        if self.experiment_settings.experiment_type == self.experiment_types.LEARNING_EXPERIMENT:
            round_logs = self.file_paths_obj.round_log_filepaths
            learn_logs_cm = self.file_paths_obj.learn_log_filepaths_cm
            learn_logs_g = self.file_paths_obj.learn_log_filepaths_g
            parsed_data_filepaths = self.file_paths_obj.parsed_data_filepaths
            processed_data_filepaths = self.file_paths_obj.processed_data_filepaths

            if not self.use_preloaded_parsed:
                parsed_data = self.parse_data(round_logs, learn_logs_cm, learn_logs_g, parsed_data_filepaths)
            else:
                parsed_data = self.load_parsed_data()
            if not self.use_preloaded_processed:
                processed_data = self.process_data(parsed_data, processed_data_filepaths)
            else:
                processed_data = self.load_processed_data()

            self.visualize_data(processed_data)
            self.compile_data()

        elif self.experiment_settings.experiment_type == self.experiment_types.PARAMETER_EXPERIMENT:
            
            final_processed_data = {}
            for i in range(len(self.experiment_settings.independent_variable)):

                round_logs = self.file_paths_obj.round_log_filepaths[i]

                parsed_data_filepaths = self.file_paths_obj.parsed_data_filepaths[i]
                #Thise will all belong to the same directory, so I can just grab the first one
                head = os.path.split(parsed_data_filepaths[0])[0]
                if not os.path.exists(head):
                    os.makedirs(head)
                
                processed_data_filepaths = self.file_paths_obj.processed_data_filepaths[i]
                head = os.path.split(processed_data_filepaths[0])[0]
                if not os.path.exists(head):
                    os.makedirs(head)

                if not self.use_preloaded_parsed:
                    parsed_data = self.parse_data(round_logs, [], [], parsed_data_filepaths)
                else:
                    parsed_data = self.load_parsed_data(None, None, None, parsed_data_filepaths)
                if not self.use_preloaded_processed:
                    processed_data = self.process_data(parsed_data, processed_data_filepaths)
                else:
                    processed_data = self.load_processed_data(None, processed_data_filepaths)

                final_processed_data[i] = processed_data

            if not self.use_preloaded_visualized:
                self.visualize_data(final_processed_data)

            self.compile_data()
        else: #this is a tournament
            round_logs = self.file_paths_obj.round_log_filepaths
            parsed_data_filepaths = self.file_paths_obj.parsed_data_filepaths
            processed_data_filepaths = self.file_paths_obj.processed_data_filepaths

            if not self.use_preloaded_parsed:
                parsed_data = self.parse_data(round_logs, [], [], parsed_data_filepaths)
            else:
                parsed_data = self.load_parsed_data()
            if not self.use_preloaded_processed:
                processed_data = self.process_data(parsed_data, processed_data_filepaths)
            else:
                processed_data = self.load_processed_data()

            self.visualize_data(processed_data)
            self.compile_data()
    
    #HELPER FUNCTIONS

    def create_param_vs_score_figures(self, processed_data):
        #each key in processed data prepresents a different parameter (e.g. 0 = 0, 1 = .001, etc.)
        parameters = self.experiment_settings.independent_variable 
        stats_vals = {}

        #loop through all of the parameter indices 
        for i in range(len(processed_data)):
            final_for_param = processed_data[i]["Final"]
            for stat in self.main_stats_keys:
                #if the cm is ensemble, then compute it's average performance against all of the other guessers 
                #save the figure for cm and this stat in the correct place 
                ens_cm = self.find_ensemble(final_for_param.keys())
                if ens_cm != None: #then there is an ensemble codemaster 
                    if "cm" not in stats_vals:
                        stats_vals["cm"] = {}
                    if stat not in stats_vals["cm"]:
                        stats_vals["cm"][stat] = []

                    values = []
                    for g in final_for_param[ens_cm]:
                        values.append(final_for_param[ens_cm][g][stat])
                    stats_vals["cm"][stat].append(np.mean(values))
            
                #if the g is ensemble, then compute it's average performance against all of the other codemasters
                ens_g = self.find_ensemble(final_for_param[list(final_for_param.keys())[0]].keys())
                if ens_g != None: #then there is an ensemble codemaster 
                    if "g" not in stats_vals:
                        stats_vals["g"] = {}
                    if stat not in stats_vals["g"]:
                        stats_vals["g"][stat] = []

                    values = []
                    for cm in final_for_param:
                        values.append(final_for_param[cm][ens_g][stat])
                    stats_vals["g"][stat].append(np.mean(values))
        
        for b_type in stats_vals:
            for stat in stats_vals[b_type]:
                fp = self.file_paths_obj.param_comparison_fig_filepaths[b_type]['final'][stat][0]
                head = os.path.split(fp)[0]
                if not os.path.exists(head):
                    os.makedirs(head)

                y = stats_vals[b_type][stat]
                plt.plot(parameters, y)
                plt.savefig(fp)
                plt.clf()

    def create_progression_plots(self, processed_data, lp, performance_stats, file_paths_dict, stats):

        for stat in stats:
            for cm in processed_data:
                #if the cm is random
                if self.is_rand_ens(cm):
                    continue
                fps = []
                has_ens_cm = False
                if self.bot_ai_types.get_bot_ai_type(cm) == self.ai_types.DISTANCE_ENSEMBLE or \
                    self.bot_ai_types.get_bot_ai_type(cm) == self.ai_types.ASSOCIATOR_ENSEMBLE:
                    fps.append(file_paths_dict['cm'][stat][lp])
                    has_ens_cm = True

                for g in processed_data[cm]:
                    if self.is_rand_ens(g):
                        continue
                    has_ens_g = False
                    if self.bot_ai_types.get_bot_ai_type(g) == self.ai_types.DISTANCE_ENSEMBLE or \
                        self.bot_ai_types.get_bot_ai_type(g) == self.ai_types.ASSOCIATOR_ENSEMBLE:
                        fps.append(file_paths_dict['g'][stat][lp])
                        has_ens_g = True 
                    
                    best_avg_cm_score = None 
                    best_avg_cm = None
                    best_avg_g_score = None 
                    best_avg_g = None


                    if has_ens_cm and not has_ens_g:
                        #then I want to find the best average codemaster 
                        best_avg_cm = performance_stats[self.conversion[stat]][self.stat_dict_keys.BEST_AVG][self.stat_dict_keys.CODEMASTER]
                        best_avg_cm_score = performance_stats[self.stat_dict_keys.SOLO_BOT_DATA][best_avg_cm][g][self.conversion[stat]]

                        #I also need to find the best possible score
                        best_overall_cm_score_for_g = performance_stats[self.conversion[stat]][self.stat_dict_keys.BEST_OVERALL][self.stat_dict_keys.CODEMASTER][g]
                        
                    
                    if has_ens_g and not has_ens_cm:
                        best_avg_g = performance_stats[self.conversion[stat]][self.stat_dict_keys.BEST_AVG][self.stat_dict_keys.GUESSER]
                        best_avg_g_score = performance_stats[self.stat_dict_keys.SOLO_BOT_DATA][cm][best_avg_g][self.conversion[stat]]

                        best_overall_g_score_for_cm = performance_stats[self.conversion[stat]][self.stat_dict_keys.BEST_OVERALL][self.stat_dict_keys.GUESSER][cm]
                    
                    if has_ens_cm:
                        #get the rand ens cm data 
                        rand_cm = self.find_rand_bot(processed_data.keys())
                        rand_ens_cm_scores = processed_data[rand_cm][g][stat]
                    if has_ens_g:
                        rand_g = self.find_rand_bot(list(processed_data[list(processed_data.keys())[0]].keys()))
                        rand_ens_g_scores = processed_data[cm][rand_g][stat]
                    
                    
                    #Now we do the actual figure creation

                    if stat == "Bot Pairing Scores":
                        yl = "CoLT Rating"
                    else:
                        yl = stat

                    data = processed_data[cm][g][stat]
                    x = list(range(1, len(data) + 1))
                    plt.plot(x, data, label="ACE")
                    if has_ens_cm and not has_ens_g:
                        if self.bot_lm_types.get_bot_lm_type(best_avg_cm) != self.bot_lm_types.get_bot_lm_type(g): plt.axhline(y = best_avg_cm_score, color='r', linestyle=':', label="BA")
                        plt.axhline(y = best_overall_cm_score_for_g, color='r', linestyle='solid', label="B")
                    if has_ens_g and not has_ens_cm:
                        if self.bot_lm_types.get_bot_lm_type(best_avg_g) != self.bot_lm_types.get_bot_lm_type(cm): plt.axhline(y = best_avg_g_score, color='r', linestyle=':', label="BA")
                        plt.axhline(y = best_overall_g_score_for_cm, color='r', linestyle='solid', label="B")
                    if has_ens_cm:
                        plt.plot(x, rand_ens_cm_scores, color='c', linestyle='solid', label="R")
                    if has_ens_g and not has_ens_cm:
                        plt.plot(x, rand_ens_g_scores, color='c', linestyle='solid', label="R")
                    elif has_ens_g:
                        plt.plot(x, rand_ens_g_scores, color='k', linestyle='solid', label="R")

                    fsize = 20
                    plt.xlabel('Game', fontsize=fsize)
                    plt.ylabel(yl, fontsize=fsize)
                    max_ticks = 6  # Set the maximum number of ticks to display
                    plt.gca().xaxis.set_major_locator(MaxNLocator(max_ticks))
                    # plt.title(cm + " + " + g)


                    plt.xticks(fontsize=fsize)
                    plt.yticks(fontsize=fsize)

                    plt.legend(fontsize=fsize)
                    for fp in fps:
                        fp += "_" + cm + "+" + g + ".jpg"
                        if not os.path.exists(os.path.dirname(fp)):
                            os.makedirs(os.path.dirname(fp))
                        plt.savefig(fp)
                    plt.clf()

                    if has_ens_g: del fps[-1]

    def create_performance_progression_sliding_window_figures(self, processed_data, lp, performance_stats):

        self.create_progression_plots(processed_data, lp, performance_stats, self.file_paths_obj.performance_progression_sliding_window_filepaths, self.performance_progression_sliding_window_stat_keys)

    def create_performance_progression_figures(self, processed_data, lp, performance_stats):

        self.create_progression_plots(processed_data, lp, performance_stats, self.file_paths_obj.performance_progression_filepaths, self.performance_progression_stat_keys)
    
    def create_single_arm_weights_figure(self, arm_weights, cm, g, save_path):
        for tm in arm_weights:
            tm_weights = arm_weights[tm]
            x_axis = list(range(len(tm_weights)))
            #replace occurrances of inf with 4
            tm_weights = [4.0 if w == np.inf else w for w in tm_weights]
            plt.plot(x_axis, tm_weights, label=tm)
        plt.legend()
        # plt.title(f"arm weights with \n{cm} and \n{g}")
        # plt.ylabel('score')
        # plt.xlabel('game')
        plt.savefig(save_path)
        plt.clf()
    
    def graph_bar_chart(self, x_axis, y_axis, title, x_label, y_label, save_file):
        fig, ax = plt.subplots() #layout="constrained"
        
        #change the x axis labels to discard the ai type
        sub_strings = ["distance associator", "baseline guesser"]
        new_x = []
        for e in x_axis:
            indices = [e.find(sub_string) for sub_string in sub_strings]
            index = max(indices)
            if index != -1:
                new_x.append(e[:index].strip())
            else:
                new_x.append(e)

        ax.bar(new_x, y_axis)
        # plt.title(title)
        # plt.ylabel(y_label)
        # plt.xlabel(x_label)
        plt.xticks(rotation = -45, fontsize = 10)
        plt.savefig(save_file)
        plt.clf() 

    def create_single_arm_percentage_figure(self, arm_percentages, cm, g, save_path):
        x_axis = []
        y_axis = []
        for arm in arm_percentages:
            x_axis.append(arm)
            y_axis.append(arm_percentages[arm])
        title = f"arm percentages with\n{cm} and\n{g}"
        x_label = "bots"
        y_label = "percentage"
        self.graph_bar_chart(x_axis, y_axis, title, x_label, y_label, save_path)

    def create_arm_weights_figures(self, processed_data, lp):
        #determine if there is an ensemble cm 
        #if there is, then grab the percent selected and plot them under arm_weights_filepaths['cm']['g'][lp]
        ens_cm = self.find_ensemble(processed_data.keys())
        if ens_cm != None:
            for g in processed_data[ens_cm]:
                #create a plot for this match up
                path = self.file_paths_obj.arm_weights_filepaths['cm'] + f"-{ens_cm}-{g}.jpg"
                arm_weights = processed_data[ens_cm][g][self.stat_dict_keys.CM_LEARN_STATS][self.stats.ARM_WEIGHTS_BY_GAME]
                self.create_single_arm_weights_figure(arm_weights, ens_cm, g, path)

        #determine if there is an ensemble g
        #if there is, then grab the percent selected and plot them under arm_weights_filepaths['g'][lp]
        ens_g = self.find_ensemble(processed_data[list(processed_data.keys())[0]].keys())
        if ens_g != None:
            for cm in processed_data:
                #create a plot for this team
                path = self.file_paths_obj.arm_weights_filepaths['g'] + f"-{cm}-{ens_g}.jpg"
                arm_weights = processed_data[cm][ens_g][self.stat_dict_keys.G_LEARN_STATS][self.stats.ARM_WEIGHTS_BY_GAME]
                self.create_single_arm_weights_figure(arm_weights, cm, ens_g, path)

    
    def create_arm_percentage_figures(self, processed_data, lp):
        #determine if there is an ensemble cm 
        #if there is, then grab the arm weights and plot them under arm_weights_filepaths['cm'][lp]
        ens_cm = self.find_ensemble(processed_data.keys())
        if ens_cm != None:
            for g in processed_data[ens_cm]:
                #create a plot for this match up
                path = self.file_paths_obj.percent_selected_filepaths['cm'] + f"{ens_cm}-{g}.jpg"
                percent_selected = processed_data[ens_cm][g][self.stat_dict_keys.CM_LEARN_STATS][self.stats.PERCENTAGE_BOT_CHOSEN]
                self.create_single_arm_percentage_figure(percent_selected, ens_cm, g, path)

        #determine if there is an ensemble g
        #if there is, then grab the arm weights and plot them under arm_weights_filepaths['g'][lp]
        ens_g = self.find_ensemble(processed_data[list(processed_data.keys())[0]].keys())
        if ens_g != None:
            for cm in processed_data:
                #create a plot for this team
                path = self.file_paths_obj.percent_selected_filepaths['g'] + f"{cm}-{ens_g}.jpg"
                percent_selected = processed_data[cm][ens_g][self.stat_dict_keys.G_LEARN_STATS][self.stats.PERCENTAGE_BOT_CHOSEN]
                self.create_single_arm_percentage_figure(percent_selected, cm, ens_g, path)

        pass
    
    def create_learn_table(self, processed_data, fp):


        #read in solo bot table
        with open(self.file_paths_obj.dist_assoc_solitair_table_path, 'r') as f:
            solo_bot_data = json.load(f)

        #Create the base table for each stat
        #determine needed solitair bots (all of the codemasters and guessers that aren't ensembles)
        has_ensemble_cm = False 
        has_ensemble_g = False
        for cm in processed_data:
            if self.ai_types.DISTANCE_ENSEMBLE == self.bot_ai_types.get_bot_ai_type(cm) or \
                self.ai_types.ASSOCIATOR_ENSEMBLE == self.bot_ai_types.get_bot_ai_type(cm):
                has_ensemble_cm = True 
        
        for g in processed_data[list(processed_data.keys())[0]]:
            if self.ai_types.DISTANCE_ENSEMBLE == self.bot_ai_types.get_bot_ai_type(g) or \
                self.ai_types.ASSOCIATOR_ENSEMBLE == self.bot_ai_types.get_bot_ai_type(g):
                has_ensemble_g = True
        
        #Now I need to calculate average performances, best avg performance, best overall performance for each stat
        performance_stats = self.calculate_performance_stats(solo_bot_data, has_ensemble_cm, has_ensemble_g)

        #if there is an ensemble cm, include avg cm performance, best cm for g (not including ensemble), best avg cm, and avg cm performance (in the columns)
        #if there ins an ensemble g, include avg g performance, best g for cm (not including ensemble), best avg g, and avg g performance (in the rows)
        #add needed columns/rows for type of ensemble bots included

        tables = {}
        for stat in self.main_stats_keys:
            tables[stat] = self.assemble_learn_table(processed_data, solo_bot_data, performance_stats, stat, has_ensemble_cm, \
                has_ensemble_g)

        #We start with adding the 
        #Save table
        #open file here and pass it into the function 
        with open(fp, "w+") as f:
            self.save_tables(tables, f)
        
        return performance_stats

    
    def save_tables(self, tables, f):
        #I can also save other files if I want 
        # with open("tables.json", 'w+') as file:
        #     json.dump(tables, file)

        #loop through the stat tables and save each one to the opened file
        for stat in tables:
            f.write(stat + '\n')
            f.write(tabulate(tables[stat], headers='firstrow', stralign='center', tablefmt='fancy_grid', floatfmt='.4f') + '\n\n')
            # f.write(tabulate(tables[stat], headers='firstrow', stralign='center', tablefmt='latex', floatfmt='.4f') + '\n\n')
    
    def merge_with_performance_stats(self, table, performance_stats, solo_bot_data, stat, has_ensemble_cm, has_ensemble_g):
        #add the needed columns
        #if ensemble cm, add Avg performance
        #if ensemble g, Best overall, Best Avg
        needed_cols = []
        num_guessers = len(table[0]) - 1
        num_codemasters = len(table) - 1

        if has_ensemble_cm:
            needed_cols.append(self.stat_dict_keys.AVG_PERF)
        if has_ensemble_g:
            needed_cols.append(self.stat_dict_keys.BEST_OVERALL)
            needed_cols.append(self.stat_dict_keys.BEST_AVG)

        #add needed rows
        #if ensemble cm, Best overall and Best Avg
        #if ensemble g, Avg performance
        needed_rows = []

        if has_ensemble_g:
            needed_rows.append(self.stat_dict_keys.AVG_PERF)
        if has_ensemble_cm:
            needed_rows.append(self.stat_dict_keys.BEST_OVERALL)
            needed_rows.append(self.stat_dict_keys.BEST_AVG)

        #now we add the needed columns 
        best_avg_col = None
        best_avg_col_vals = []
        for i in range(len(needed_cols)):
            #append the new column to the table
            if needed_cols[i] == self.stat_dict_keys.BEST_AVG:
                best_avg_col = len(table[0])

            table[0].append(needed_cols[i])
            #loop through the rows
            for j in range(1, len(table)):
                if i == 0 and len(needed_cols) != 2: #The codemaster column will always be first
                    table[j].append(round(performance_stats[stat][needed_cols[i]][self.stat_dict_keys.CODEMASTER][table[j][0]], self.precision))
                if (len(needed_cols)) == 2 or (len(needed_cols) == 3 and i != 0):
                    if needed_cols[i] != self.stat_dict_keys.BEST_AVG:
                        table[j].append(round(performance_stats[stat][needed_cols[i]][self.stat_dict_keys.GUESSER][table[j][0]], self.precision))
                    else:
                        g = performance_stats[stat][needed_cols[i]][self.stat_dict_keys.GUESSER]
                        if self.bot_lm_types.get_bot_lm_type(g) != self.bot_lm_types.get_bot_lm_type(table[j][0]):
                            table[j].append(round(solo_bot_data[table[j][0]][g][stat], self.precision))
                            best_avg_col_vals.append(round(solo_bot_data[table[j][0]][g][stat], self.precision))
                        else:
                            table[j].append('-')

        #now we add the needed rows
        best_avg_row = None
        best_avg_row_vals = []
        for i in range(len(needed_rows)):
            if needed_rows[i] == self.stat_dict_keys.BEST_AVG:
                best_avg_row = len(table)

            table.append([needed_rows[i]])
            #loop through the columns
            for j in range(1, len(table[0])):
                if i == 0 and len(needed_rows) != 2 and (j < (len(table[0]) - len(needed_cols))): 
                    table[-1].append(round(performance_stats[stat][needed_rows[i]][self.stat_dict_keys.GUESSER][table[0][j]], self.precision))
                elif ((len(needed_rows) == 2) or (len(needed_rows) == 3 and i != 0)) and (j < (len(table[0]) - len(needed_cols))):
                    if needed_rows[i] != self.stat_dict_keys.BEST_AVG:
                        table[-1].append(round(performance_stats[stat][needed_rows[i]][self.stat_dict_keys.CODEMASTER][table[0][j]], self.precision))
                    else:
                        cm = performance_stats[stat][needed_rows[i]][self.stat_dict_keys.CODEMASTER]
                        #Check to see if this is against the same bot 
                        if self.bot_lm_types.get_bot_lm_type(cm) != self.bot_lm_types.get_bot_lm_type(table[0][j]):
                            table[-1].append(round(solo_bot_data[cm][table[0][j]][stat], self.precision))
                            best_avg_row_vals.append(round(solo_bot_data[cm][table[0][j]][stat], self.precision))
                        else:
                            table[-1].append('-')
                else:
                    table[-1].append('-')
        
        #add averages to the table as needed 
        if best_avg_col != None:
            table[num_codemasters + 1][best_avg_col] = round(np.mean(best_avg_col_vals), self.precision)
        if best_avg_row != None:
            table[best_avg_row][num_guessers + 1] = round(np.mean(best_avg_row_vals), self.precision)

    
    def find_ensemble(self, d):
        ensemble = None
        for bot in d:
            if (self.ai_types.DISTANCE_ENSEMBLE == self.bot_ai_types.get_bot_ai_type(bot) or \
                self.ai_types.ASSOCIATOR_ENSEMBLE == self.bot_ai_types.get_bot_ai_type(bot)):
                ensemble = bot
                break  
        return ensemble


    def is_rand_ens(self, bot):
        if self.bot_ai_types.get_bot_ai_type(bot) == self.ai_types.RANDOM_DISTANCE_ENSEMBLE or \
                        self.bot_ai_types.get_bot_ai_type(bot) == self.ai_types.RANDOM_ASSOCIATOR_ENSEMBLE:
            return True 
        return False
    
    def find_rand_bot(self, bots):
        #search through a list of bots and check their bot types. If they are rand, return it, otherwise return None 
        for bot in bots:
            if self.is_rand_ens(bot):
                return bot
        return

    def round_val(self, v):
        if isinstance(v, tuple) or isinstance(v, list):
            v = [round(t, self.precision) for t in v]
        else:
            v = round(v, self.precision)
        return v

    def merge_with_rand_data(self, table, processed_data, stat):
        #I know that the processed data doesn't have lps anymore 
        i = 0
        #if there is a rand cm, I need to add a row to the table
        rand_cm = self.find_rand_bot(processed_data.keys())
        if rand_cm != None:
            #then add the row 
            row = [rand_cm]
            for g in table[0][1:8]:
                v = self.get_val(processed_data[rand_cm][g][stat])
                #do the rounding on val
                row.append(self.round_val(v))
            #we now calculate the average 

            if isinstance(row[1], tuple) or isinstance(row[1], list):
                l = [i[0] for i in row[1:]]
                avg = round(np.average(l), self.precision)
            else:
                avg = round(np.average(row[1:]), self.precision)
            row.append(avg)
            table.append(row)

        #if there is a rand guesser, I need to add the rand guesser column to the end of all of the rows 
        rand_g = self.find_rand_bot(processed_data[list(processed_data.keys())[0]])
        if rand_g != None:
            #then add the column 
            column_vals = [rand_g]
            for cm in [row[0] for row in table[1:8]]:
                v = self.get_val(processed_data[cm][rand_g][stat])
                column_vals.append(self.round_val(v))
            #We take the average and append it 
            if isinstance(column_vals[1], tuple) or isinstance(column_vals[1], list):
                l = [i[0] for i in column_vals[1:]]
                avg = round(np.average(l), self.precision)
            else:
                avg = round(np.average(column_vals[1:]), self.precision)
            column_vals.append(avg)
            for row, c_val in zip(table, column_vals):
                row.append(c_val)
        
        #I need to put in the dashes that are needed 
        if rand_cm != None:
            #Then I add 3 dashes 
            for i in range(2):
                table[-1].append('-')
        
        if rand_g != None:
            start = len(table) - 3
            for i in range(start, start + 2):
                table[i].append('-')

        if rand_cm != None and rand_g != None:
            #put in the bottom cor
            v = self.get_val(processed_data[rand_cm][rand_g][stat])
            table[-1].append(self.round_val(v))

    def get_val(self, value):
        if isinstance(value, tuple) or isinstance(value, list):
            v = value[0]
        else:
            v = value 
        return v

    def merge_with_processed_data(self, table, processed_data, stat, has_ensemble_cm, has_ensemble_g):
        ensemble_cm = None 
        ensemble_g = None

        if has_ensemble_cm:
            #find the bot that is an ensemble
            ensemble_cm = self.find_ensemble(list(processed_data.keys()))
            assert(ensemble_cm != None)
            
            #add a new row
            table.append([ensemble_cm])

            vals = []
            done_avg = False
            for i in range(1, len(table[0])):
                if done_avg:
                    table[-1].append('-')
                    continue
                if table[0][i] not in processed_data[ensemble_cm] and not done_avg:
                    done_avg = True
                    #Then we have looped through all of the bots and we need to append the average
                    table[-1].append(round(np.mean(vals), self.precision))
                    continue

                v = self.get_val(processed_data[ensemble_cm][table[0][i]][stat])

                table[-1].append(self.round_val(v))

                if isinstance(v, tuple) or isinstance(v, list):
                    vals.append(self.round_val(v)[0])
                else:
                    vals.append(self.round_val(v))

        if has_ensemble_g:
            ensemble_g = self.find_ensemble(processed_data[list(processed_data.keys())[0]])
            assert(ensemble_g != None)

            #add new col
            table[0].append(ensemble_g)

            vals = []
            done_avg = False 
            for i in range(1, len(table)):
                if done_avg:
                    table[i].append('-')
                    continue 
                if table[i][0] not in processed_data and not done_avg:
                    done_avg = True 
                    table[i].append(round(np.mean(vals), self.precision))
                    continue 
                
                v = self.get_val(processed_data[table[i][0]][ensemble_g][stat])
                table[i].append(self.round_val(v))

                if isinstance(v, tuple) or isinstance(v, list):
                    vals.append(self.round_val(v)[0])
                else:
                    vals.append(self.round_val(v))
        
        if has_ensemble_g:
            rand_cm = self.find_rand_bot(processed_data.keys())
            v = self.get_val(processed_data[rand_cm][ensemble_g][stat])
            table[-2][-1] = self.round_val(v)
        
        if has_ensemble_cm:
            rand_g = self.find_rand_bot(processed_data[list(processed_data.keys())[0]])
            v = self.get_val(processed_data[ensemble_cm][rand_g][stat])
            table[-1][-2] = self.round_val(v)
        
        #Now we add the ensemble vs ensemble if it exists
        if has_ensemble_cm and has_ensemble_g:
            v = self.get_val(processed_data[ensemble_cm][ensemble_g][stat])
            table[-1][-1] = self.round_val(v)
            

    def assemble_learn_table(self, processed_data, solo_bot_data, performance_stats, stat, has_ensemble_cm, has_ensemble_g):
        table = self.assemble_main_table(solo_bot_data, stat)

        #add in other stuff
        self.merge_with_performance_stats(table, performance_stats, solo_bot_data, stat, has_ensemble_cm, has_ensemble_g)
        self.merge_with_rand_data(table, processed_data, stat)
        self.merge_with_processed_data(table, processed_data, stat, has_ensemble_cm, has_ensemble_g)

        return table
    
    ###NOTE: Make sure that the processed data passed in doesn't have an lp layer in the dictionary
    def assemble_main_table(self, processed_data, stat):
        #loop throught the cms and then loop through the gs
        table = []

        codemasters = list(processed_data.keys())
        guessers = list(processed_data[codemasters[0]].keys())

        #sort them to ensure that the bots line up correctly 
        codemasters = sorted(codemasters, reverse=True)
        guessers = sorted(guessers, reverse=True)

        headers = copy.deepcopy(guessers)
        headers.insert(0, "cm/g")

        for i in range(len(codemasters)):
            table.append([codemasters[i]])
            for j in range(len(guessers)):
                if self.experiment_settings.include_same_lm or (self.bot_lm_types.get_bot_lm_type(codemasters[i]) != self.bot_lm_types.get_bot_lm_type(guessers[j])):
                    table[i].append(round(processed_data[codemasters[i]][guessers[j]][stat], self.precision))
                else:
                    table[i].append('-')

        table.insert(0, headers)
                
        #meanwhile 
        return table

    def create_main_table(self, processed_data, fp):
        #This creates a cross table with the averages of the performances for cms and gs
        tables = {}
        for stat in self.main_stats_keys:
            tables[stat] = self.assemble_main_table(processed_data, stat)
        #Save stuff

    def merge_data(self, merged_dict, learning_dict, type):
        for cm in merged_dict:
            for g in merged_dict[cm]:
                if type == types.CM and (self.ai_types.DISTANCE_ENSEMBLE == self.bot_ai_types.get_bot_ai_type(cm) or \
                    self.ai_types.ASSOCIATOR_ENSEMBLE == self.bot_ai_types.get_bot_ai_type(cm)):
                    merged_dict[cm][g][self.stat_dict_keys.CM_LEARN_STATS] = learning_dict[g]
                elif type == types.G and (self.ai_types.DISTANCE_ENSEMBLE == self.bot_ai_types.get_bot_ai_type(g) or \
                    self.ai_types.ASSOCIATOR_ENSEMBLE == self.bot_ai_types.get_bot_ai_type(g)):
                    merged_dict[cm][g][self.stat_dict_keys.G_LEARN_STATS] = learning_dict[cm]

    def compare_to_best(self, best, val, stat):
        if self.desired_stats.get_desired_stats(stat)[self.desired_stats_keys.OPTIMAL_EXTREME] == self.min_max_keys.MIN:
            if val < best:
                return val
            else:
                return best
        else:
            if val > best:
                return val
            else:
                return best
    
    def set_best(self, stat):
        if self.desired_stats.get_desired_stats(stat)[self.desired_stats_keys.OPTIMAL_EXTREME] == self.min_max_keys.MIN:
            best = np.inf 
        else:
            best = -np.inf 
        return best


    def calculate_performance_stats(self, solo_bot_data, has_ensemble_cm, has_ensemble_g):
        #Now I need to calculate average performances, best avg performance, best overall performance for each stat

        performance_stats = {}
        performance_stats[self.stat_dict_keys.SOLO_BOT_DATA] = solo_bot_data
        for stat in self.main_stats_keys:
            
            if stat not in performance_stats:
                performance_stats[stat] = {
                    self.stat_dict_keys.BEST_AVG: {},
                    self.stat_dict_keys.BEST_OVERALL: {},
                    self.stat_dict_keys.AVG_PERF: {}
                }

            if has_ensemble_cm:

                best = self.set_best(stat)

                #Caclulate average performances
                #I need all of the average cm performances accross guessers
                best_cm = None
                best_overall_cm_for_g = {}
                for cm in solo_bot_data:
                    values = []
                    for g in solo_bot_data[cm]:

                        #We check to see if the two bots have the same underlying language models
                        if not self.experiment_settings.include_same_lm and \
                            self.bot_lm_types.get_bot_lm_type(cm) == self.bot_lm_types.get_bot_lm_type(g):
                            continue

                        values.append(solo_bot_data[cm][g][stat])

                        #We can also take care of finding the best overall cm for g
                        if g not in best_overall_cm_for_g:
                            best_overall_cm_for_g[g] = self.set_best(stat)
                        best_overall_cm_for_g[g] = self.compare_to_best(best_overall_cm_for_g[g], solo_bot_data[cm][g][stat], stat)

                    avg_v = round(np.mean(values), self.precision)

                    t_best = self.compare_to_best(best, avg_v, stat)

                    if best != t_best:
                        #then we have a new best cm
                        best_cm = cm 
                    best = t_best

                    if self.stat_dict_keys.CODEMASTER not in performance_stats[stat][self.stat_dict_keys.AVG_PERF]:
                        performance_stats[stat][self.stat_dict_keys.AVG_PERF][self.stat_dict_keys.CODEMASTER] = {}
                    performance_stats[stat][self.stat_dict_keys.AVG_PERF][self.stat_dict_keys.CODEMASTER][cm] = avg_v
                    

                #Now we set the value for the best avg performance
                performance_stats[stat][self.stat_dict_keys.BEST_AVG][self.stat_dict_keys.CODEMASTER] = best_cm

                #now we set the value for the best overall values
                performance_stats[stat][self.stat_dict_keys.BEST_OVERALL][self.stat_dict_keys.CODEMASTER] = best_overall_cm_for_g

            if has_ensemble_g:

                best = self.set_best(stat)

                #Caclulate average performances
                #I need all of the average g performances accross guessers
                best_g = None
                best_overall_g_for_cm = {}
                for g in solo_bot_data[list(solo_bot_data.keys())[0]]:
                    values = []
                    for cm in solo_bot_data:
                        
                        #We check if the two bots have the same underlying language models
                        if not self.experiment_settings.include_same_lm and \
                            self.bot_lm_types.get_bot_lm_type(cm) == self.bot_lm_types.get_bot_lm_type(g):
                            continue

                        values.append(solo_bot_data[cm][g][stat])

                        #We can also take care of finding the best overall cm for g
                        if cm not in best_overall_g_for_cm:
                            best_overall_g_for_cm[cm] = self.set_best(stat)
                        best_overall_g_for_cm[cm] = self.compare_to_best(best_overall_g_for_cm[cm], solo_bot_data[cm][g][stat], stat)

                    avg_v = round(np.mean(values), self.precision)

                    t_best = self.compare_to_best(best, avg_v, stat)

                    if best != t_best:
                        #then we have a new best cm
                        best_g = g 
                    best = t_best

                    if self.stat_dict_keys.GUESSER not in performance_stats[stat][self.stat_dict_keys.AVG_PERF]:
                        performance_stats[stat][self.stat_dict_keys.AVG_PERF][self.stat_dict_keys.GUESSER] = {}
                    performance_stats[stat][self.stat_dict_keys.AVG_PERF][self.stat_dict_keys.GUESSER][g] = avg_v

                #Now we set the value for the best avg performance
                performance_stats[stat][self.stat_dict_keys.BEST_AVG][self.stat_dict_keys.GUESSER] = best_g

                #now we set the value for the best overall values
                performance_stats[stat][self.stat_dict_keys.BEST_OVERALL][self.stat_dict_keys.GUESSER] = best_overall_g_for_cm
        
        return performance_stats
    
    def load_processed_data(self):
        processed_data = {}
        counter = 0
        for filepath in self.file_paths_obj.processed_data_filepaths[:-1]:
            try:
                with open(filepath, 'r') as f:
                    processed_data[counter] = json.load(f)
            except:
                counter += 1
                continue
            counter += 1
        with open(self.file_paths_obj.processed_data_filepaths[-1], 'r') as f:
            processed_data[self.stat_dict_keys.FINAL_KEY] = json.load(f)
        return processed_data

    def load_parsed_data(self):
        parsed_data = {}
        counter = 0
        for filepath in self.file_paths_obj.parsed_data_filepaths:
            try:
                with open(filepath, 'r') as f:
                    parsed_data[counter] = json.load(f)
            except:
                counter += 1
                continue
            counter += 1
        return parsed_data
    
    def get_win_times(self, game_win_loss, num_rounds_per_game):
        win_times = []
        for i in range(len(game_win_loss)):
            if game_win_loss[i] == 1:
                win_times.append(int(num_rounds_per_game[i]))
        return win_times

    def create_string(self, arr):
        res = ''
        for num in arr:
            res += str(num)
        return res

    def generate_pos_events(self):
        res = []
        for r in range(10):
            c = 0
            for b in [None, 'theirs', 'by', 'assassin']:
                
                if r == 0 and (b is None):
                    c += 1
                    continue
                if r == 9 and (b is not None):
                    c += 1
                    continue

                key = [r, 0, 0, 0]
                if c > 0:
                    key[c] = 1
                c += 1
                res.append(self.create_string(key))
        return res

    def get_feature_vec(self, occurance_dict, pos_events):
        x = []
        total_events = sum(occurance_dict.values())
        for e in pos_events:
            if total_events != 0:
                x.append(occurance_dict[e] / total_events)
            else:
                x.append(0)
        return x
    
    def get_event_arrays(self, num_rounds_per_game, red_words_flipped_by_round, \
        blue_words_flipped_by_round, bystander_words_flipped_by_round, assassin_words_flipped_by_round):
        event_arrays = []

        curr_ind = 0
        for i in range(len(num_rounds_per_game)):
            event_arrays.append([])
            for j in range(curr_ind, curr_ind + int(num_rounds_per_game[i])):
                rwf = red_words_flipped_by_round[j]
                bwf = blue_words_flipped_by_round[j]
                bywf = bystander_words_flipped_by_round[j]
                awf = assassin_words_flipped_by_round[j]

                event_arrays[i].append([rwf, bwf, bywf, awf])

            curr_ind += int(num_rounds_per_game[i])
        
        return event_arrays
    
    def get_pair_scores(self, num_rounds_per_game, red_words_flipped_by_round, \
        blue_words_flipped_by_round, bystander_words_flipped_by_round, assassin_words_flipped_by_round):
        
        #A dictionary that keeps thrack of all the events we've seen up until now
        events = {}

        #Generate all of the events that are possible
        pos_events = self.generate_pos_events()

        #Put those counts in a dictionary
        for e in pos_events:
            events[e] = 0
        
        #Create an arry to keep all of the pair scores for every game
        pair_scores = []

        #load the model
        model = joblib.load(self.file_paths_obj.model_path)

        event_arrays = self.get_event_arrays(num_rounds_per_game, red_words_flipped_by_round, \
            blue_words_flipped_by_round, bystander_words_flipped_by_round, assassin_words_flipped_by_round)


        for g in event_arrays:
            for round_outcome in g:
                e = self.create_string(round_outcome)
                events[e] += 1
            vec = self.get_feature_vec(events, pos_events)
            pair_scores.append(model.predict(np.array(vec).reshape(1, -1))[0])

                  

        #Now we iterate through all of the rounds and we create the turn outcome for 
        #each round. We then add an occurance to the dictionary. At the game end point
        #We put the score of that vector into the pair_scores array
        # for i in range(len(num_rounds_per_game)):
        # curr_ind = 0
        # for i in range(len(num_rounds_per_game)):
        #     for j in range(curr_ind, curr_ind + int(num_rounds_per_game[i])):
        #         rwf = red_words_flipped_by_round[j]
        #         bwf = blue_words_flipped_by_round[j]
        #         bywf = bystander_words_flipped_by_round[j]
        #         awf = assassin_words_flipped_by_round[j]
        #         #find the corresponding event and increment the count
        #         e = self.create_string([rwf, bwf, bywf, awf])
        #         events[e] += 1
        #     #Calculate the accumalative pair score at the end of that game
        #     vec = self.get_feature_vec(events, pos_events)
        #     pair_scores.append(model.predict(np.array(vec).reshape(1, -1))[0])
        #     curr_ind += int(num_rounds_per_game[i])

        return pair_scores
    
    def calculate_flips_by_game(self, parsed_data, key, lp, cm, g):
        curr_pos = 0
        flips_in_game = []
        for rounds_in_game in parsed_data[lp][cm][g][self.stats.NUM_ROUNDS_PER_GAME]:
            flipped_in_game = 0
            for i in range(curr_pos, curr_pos + rounds_in_game):
                flipped_in_game += parsed_data[lp][cm][g][key][i]
            flips_in_game.append(flipped_in_game)
            curr_pos += rounds_in_game
        return flips_in_game
    
    def calculate_arm_weights_by_game(self, parsed_data, lp, cm, g, key):
        round_arm_weights = parsed_data[lp][cm][g][key][self.stats.ARM_WEIGHTS_BY_ROUND]
        game_arm_weights = {}
        curr_pos = 0

        #Get the initial value
        for bot in round_arm_weights:
            game_arm_weights[bot] = []
            #Now add the last of each game to the list
            game_arm_weights[bot].append(round_arm_weights[bot][curr_pos])

        for rounds_in_game in parsed_data[lp][cm][g][self.stats.NUM_ROUNDS_PER_GAME]:
            #Set the new position so we can add the correct corresponding arm weights
            curr_pos += rounds_in_game
            #loop through all of the arms
            for bot in round_arm_weights:
                # Now add the last of each game to the list
                # Subtract 1 because the arm weights are added before each round
                try:
                    game_arm_weights[bot].append(round_arm_weights[bot][curr_pos - 1])
                except:
                    print("cm: ", cm, "\ng: ", g)
        
        return game_arm_weights
    
    def process_learning_data(self, processed_data, parsed_data, lp, cm, g, key):
        if key not in parsed_data[lp][cm][g]:
            return 
        #Add a new key into the data structure
        processed_data[lp][cm][g][key] = {}

        if key not in parsed_data[lp][cm][g]:
            return

        #Check the percentages of each bot chosen
        bots_chosen = parsed_data[lp][cm][g][key][self.stats.CHOSEN_BOTS_BY_ROUND]
        bot_counts = {}
        for bot in bots_chosen:
            if bot not in bot_counts:
                bot_counts[bot] = 1
            else:
                bot_counts[bot] += 1
        
        for bot in bot_counts:
            bot_counts[bot] = bot_counts[bot] / len(bots_chosen)

        processed_data[lp][cm][g][key][self.stats.PERCENTAGE_BOT_CHOSEN] = bot_counts

        #Now we need to find the arm weights by game
        processed_data[lp][cm][g][key][self.stats.ARM_WEIGHTS_BY_GAME] = self.calculate_arm_weights_by_game(parsed_data, lp, cm, g, key)
    
    def get_mean_w_moe(self, arr):
            mean = np.mean(arr) 
            n = len(arr)
            std_error = stats.sem(arr)
            #we use the t distribution to account for non-normal distributions
            t = stats.t.ppf((1 + self.confidence_level) / 2, n-1)
            margin_of_error = t * std_error 

            return mean, margin_of_error
    
    def get_averages_singles(self, averaged_data, processed_data, lps, key, cm, g):
        arr = []
        for lp in lps:
            arr.append(processed_data[lp][cm][g][key])

        averaged_data[cm][g][key] = self.get_mean_w_moe(arr)
    
    def get_averages_lists(self, averaged_data, processed_data, lps, key, cm, g):
        final_arr = []
        #We can assume all of the lists are the same size
        for i in range(len(processed_data[lps[0]][cm][g][key])):
            temp_arr= []
            for lp in lps:
                temp_arr.append(processed_data[lp][cm][g][key][i])

            final_arr.append(np.mean(temp_arr))
        averaged_data[cm][g][key] = final_arr

    
    def get_averages_dict_single(self, averaged_data, processed_data, lps, dict_key, stat_key, cm, g):
        if dict_key not in processed_data[lps[0]][cm][g]:
            return 
        val_dict = {}
        for lp in lps:
            try:
                for arm in processed_data[lp][cm][g][dict_key][stat_key]:
                    if arm not in val_dict:
                        val_dict[arm] = []
                    val_dict[arm].append(processed_data[lp][cm][g][dict_key][stat_key][arm])
            except:
                continue
        #Now loop back through the arms and take the average of the list
        for arm in val_dict:
            val_dict[arm] = np.average(val_dict[arm])

        if dict_key not in averaged_data[cm][g]:
            averaged_data[cm][g][dict_key] = {}

        averaged_data[cm][g][dict_key][stat_key] = val_dict

    def get_averages_dict_lists(self, averaged_data, processed_data, lps, dict_key, stat_key, cm, g):
        if dict_key not in processed_data[lps[0]][cm][g]:
            return 
        final_val_dict = {}
        #loop through all of the games
        for i in range(len(processed_data[lps[0]][cm][g][dict_key][stat_key][list(processed_data[lps[0]][cm][g][dict_key][stat_key].keys())[0]])):
            temp_val_dict = {}
            for lp in lps:
                try:
                    for arm in processed_data[lp][cm][g][dict_key][stat_key]:
                        if arm not in temp_val_dict:
                            temp_val_dict[arm] = []
                        temp_val_dict[arm].append(processed_data[lp][cm][g][dict_key][stat_key][arm][i])
                except:
                    continue
            for arm in temp_val_dict:
                if arm not in final_val_dict:
                    final_val_dict[arm] = []
                final_val_dict[arm].append(np.average(temp_val_dict[arm]))
        

        if dict_key not in averaged_data[cm][g]:
            averaged_data[cm][g][dict_key] = {}

        averaged_data[cm][g][dict_key][stat_key] = final_val_dict

    
    def get_averages(self, processed_data):
        averaged_data = {}

        lps = list(processed_data.keys())
        t = lps[0]
        for cm in processed_data[t]:
            if cm not in averaged_data:
                averaged_data[cm] = {}
            for g in processed_data[t][cm]:
                if g not in averaged_data[cm]:
                    averaged_data[cm][g] = {}
                #Now we loop through all of the lps to get averages for the stats
                #TODO: consider calculating confidence intervals as well

                #Average the win rates
                self.get_averages_singles(averaged_data, processed_data, lps, self.stats.WIN_RATE, cm, g)

                #Average the win times
                self.get_averages_singles(averaged_data, processed_data, lps, self.stats.AVG_WIN_TIME, cm, g)

                #Average the min win timest
                self.get_averages_singles(averaged_data, processed_data, lps, self.stats.MIN_WIN_TIME, cm, g)

                #Average the pair scores
                #TODO: Find a way to get these averages with differing length lists!!! np.nanmean()
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.PAIR_SCORES, cm, g)

                #Average the final pair scores
                self.get_averages_singles(averaged_data, processed_data, lps, self.stats.FINAL_PAIR_SCORE, cm, g)

                #Average the avg red/blue/bystander/assassin words flipped by game
                self.get_averages_singles(averaged_data, processed_data, lps, self.stats.AVG_RED_FLIP_BY_GAME, cm, g)
                self.get_averages_singles(averaged_data, processed_data, lps, self.stats.AVG_BLUE_FLIP_BY_GAME, cm, g)
                self.get_averages_singles(averaged_data, processed_data, lps, self.stats.AVG_BYSTANDER_FLIP_BY_GAME, cm, g)
                self.get_averages_singles(averaged_data, processed_data, lps, self.stats.AVG_ASSASSIN_FLIP_BY_GAME, cm, g)

                #average the red/blue/bystander/assassin words flipped by game
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.RED_FLIP_BY_GAME, cm, g)
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.BLUE_FLIP_BY_GAME, cm, g)
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.BYSTANDER_FLIP_BY_GAME, cm, g)
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.ASSASSIN_FLIP_BY_GAME, cm, g)

                #average running totals
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.RUNNING_AVG_WR, cm, g)
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.RUNNING_AVG_WT, cm, g)
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.RUNNING_AVG_RED_FLIP_BY_GAME, cm, g)
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.RUNNING_AVG_BLUE_FLIP_BY_GAME, cm, g)
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.RUNNING_AVG_BYSTANDER_FLIP_BY_GAME, cm, g)
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.RUNNING_AVG_ASSASSIN_FLIP_BY_GAME, cm, g)

                #average sliding windows
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.SLIDING_WINDOW_PAIR_SCORES, cm, g)
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.SLIDING_WINDOW_AVG_WR, cm, g)
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.SLIDING_WINDOW_AVG_WT, cm, g)
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.SLIDING_WINDOW_AVG_RED_FLIP_BY_GAME, cm, g)
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.SLIDING_WINDOW_AVG_BLUE_FLIP_BY_GAME, cm, g)
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.SLIDING_WINDOW_AVG_BYSTANDER_FLIP_BY_GAME, cm, g)
                self.get_averages_lists(averaged_data, processed_data, lps, self.stats.SLIDING_WINDOW_AVG_ASSASSIN_FLIP_BY_GAME, cm, g)

                #Take care of learn log stats
                #Check that if it's a learning experiment, if there is a cm ensemble
                if len(self.file_paths_obj.learn_log_filepaths_cm) > 0:
                    #average percentage bots chosen
                    self.get_averages_dict_single(averaged_data, processed_data, lps, self.stat_dict_keys.CM_LEARN_STATS, self.stats.PERCENTAGE_BOT_CHOSEN, cm, g)
                    #average arm weights
                    self.get_averages_dict_lists(averaged_data, processed_data, lps, self.stat_dict_keys.CM_LEARN_STATS, self.stats.ARM_WEIGHTS_BY_GAME, cm, g)

                if len(self.file_paths_obj.learn_log_filepaths_g) > 0:
                    #average percentage bots chosen
                    self.get_averages_dict_single(averaged_data, processed_data, lps, self.stat_dict_keys.G_LEARN_STATS, self.stats.PERCENTAGE_BOT_CHOSEN, cm, g)
                    #average arm weights
                    self.get_averages_dict_lists(averaged_data, processed_data, lps, self.stat_dict_keys.G_LEARN_STATS, self.stats.ARM_WEIGHTS_BY_GAME, cm, g)

        return averaged_data