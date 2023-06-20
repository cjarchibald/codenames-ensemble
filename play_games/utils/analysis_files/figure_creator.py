from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import numpy as np
import os


class FigureCreator:
    def __init__(self, stat_dict_keys, stats, check_if_ensemble, is_rand_ens, extract_val, find_rand_bot, create_path, file_paths_obj, find_ensemble, \
                 performance_progression_sliding_window_stat_keys, performance_progression_stat_keys, experiment_settings, main_stats_keys, compiled_data_keys, 
                 compiled_data_stats, final_stat_dist_keys):
        self.stat_dict_keys = stat_dict_keys
        self.stats = stats
        self.check_if_ensemble = check_if_ensemble
        self.is_rand_ens = is_rand_ens
        self.extract_val = extract_val
        self.find_rand_bot = find_rand_bot
        self.create_path = create_path
        self.file_paths_obj = file_paths_obj
        self.find_ensemble = find_ensemble
        self.performance_progression_sliding_window_stat_keys = performance_progression_sliding_window_stat_keys
        self.performance_progression_stat_keys = performance_progression_stat_keys
        self.experiment_settings = experiment_settings
        self.main_stats_keys = main_stats_keys
        self.compiled_data_keys = compiled_data_keys
        self.compiled_data_stats = compiled_data_stats
        self.fig = True
        self.final_stat_dist_keys = final_stat_dist_keys

        self.compiled_data = {} #cm, g, list of plots

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

    def create_figures(self, processed_data, lp, performance_stats):
        self.create_final_distribution_figures(processed_data, lp)
        self.create_performance_progression_figures(processed_data, lp, performance_stats)
        self.create_performance_progression_sliding_window_figures(processed_data, lp, performance_stats)
        self.create_arm_percentage_figures(processed_data, lp)
        self.create_arm_weights_figures(processed_data, lp)

    
    def assign_val(self, itr, e_ind, cm, g, stat, key):

        if e_ind == 1:
            comp = g 
            other = 0
        else: 
            comp = cm
            other = 1

        val = None 
        for e in itr:
            if e[e_ind] == comp:
                val = round(e[-1], 4)
                ob = e[other]
                break
        self.compiled_data[cm][g][self.compiled_data_keys.STAT_COMPARISON][stat][key] = (ob, val)

    def get_compiled_info(self, performance_stats, processed_data):

        #go through ever cm and g and add the corresponding 
        for stat in self.compiled_data_stats:
            for cm in processed_data:

                for g in processed_data[cm]:
                    
                    if self.is_rand_ens(cm) or self.is_rand_ens(g):
                        continue

                    if self.check_if_ensemble(cm) and not self.check_if_ensemble(g):

                        self.populate_needed_fields(self.compiled_data, [cm, g, self.compiled_data_keys.STAT_COMPARISON, stat])

                        self.assign_val(performance_stats[self.stat_dict_keys.CODEMASTER][stat][self.stat_dict_keys.BEST_AVG], 1, cm, g, stat, self.stat_dict_keys.BEST_AVG)
                        self.assign_val(performance_stats[self.stat_dict_keys.CODEMASTER][stat][self.stat_dict_keys.BEST_OVERALL], 1, cm, g, stat, self.stat_dict_keys.BEST_OVERALL)
                        self.assign_val(performance_stats[self.stat_dict_keys.CODEMASTER][stat][self.stat_dict_keys.RANDOM], 1, cm, g, stat, self.stat_dict_keys.RANDOM)
                        

                    if self.check_if_ensemble(g) and not self.check_if_ensemble(cm):

                        self.populate_needed_fields(self.compiled_data, [cm, g, self.compiled_data_keys.STAT_COMPARISON, stat])

                        self.assign_val(performance_stats[self.stat_dict_keys.GUESSER][stat][self.stat_dict_keys.BEST_AVG], 0, cm, g, stat, self.stat_dict_keys.BEST_AVG)
                        self.assign_val(performance_stats[self.stat_dict_keys.GUESSER][stat][self.stat_dict_keys.BEST_OVERALL], 0, cm, g, stat, self.stat_dict_keys.BEST_OVERALL)
                        self.assign_val(performance_stats[self.stat_dict_keys.GUESSER][stat][self.stat_dict_keys.RANDOM], 0, cm, g, stat, self.stat_dict_keys.RANDOM)

                    self.populate_needed_fields(self.compiled_data, [cm, g, self.compiled_data_keys.STAT_COMPARISON, stat])
                    self.compiled_data[cm][g][self.compiled_data_keys.STAT_COMPARISON][stat]["Self"] = round(self.extract_val(processed_data[cm][g][stat]), 4)

        return self.compiled_data


    def populate_needed_fields(self, d, fields):

        curr = d 
        for f in fields:
            if f not in curr:
                curr[f] = {}
            curr = curr[f]
    
    def create_progression_plots(self, processed_data, lp, performance_stats, file_paths_dict, stats, compile_key):

        for stat in stats:
            for cm in processed_data:

                fps = []
                has_ens_cm = False
                if self.check_if_ensemble(cm):
                    fps.append(file_paths_dict['cm'][stat][lp])
                    has_ens_cm = True

                for g in processed_data[cm]:

                    has_ens_g = False
                    if self.check_if_ensemble(g):
                        fps.append(file_paths_dict['g'][stat][lp])
                        has_ens_g = True 
                    
                    best_avg_cm_score = None 
                    best_avg_g_score = None 


                    if has_ens_cm and not has_ens_g:
                        #then I want to find the best average codemaster 
                        vals = performance_stats[self.stat_dict_keys.CODEMASTER][self.conversion[stat]][self.stat_dict_keys.BEST_AVG]
                        # I need to get the one that has the correct guesser
                        for e in vals:
                            if e[1] == g:
                                best_avg_cm_score = e[-1]
                                break

                        #I also need to find the best possible score
                        
                        vals = performance_stats[self.stat_dict_keys.CODEMASTER][self.conversion[stat]][self.stat_dict_keys.BEST_OVERALL]
                        for e in vals:
                            if e[1] == g:
                                best_overall_cm_score_for_g = e[-1]
                                break
                        
                    
                    if has_ens_g and not has_ens_cm:
                        vals = performance_stats[self.stat_dict_keys.GUESSER][self.conversion[stat]][self.stat_dict_keys.BEST_AVG]
                        for e in vals:
                            if e[0] == cm:
                                best_avg_g_score = e[-1]
                                break 

                        vals = performance_stats[self.stat_dict_keys.GUESSER][self.conversion[stat]][self.stat_dict_keys.BEST_OVERALL]
                        for e in vals:
                            if e[0] == cm:
                                best_overall_g_score_for_cm = e[-1]

                    if has_ens_cm:
                        #get the rand ens cm data 
                        rand_cm = self.find_rand_bot(processed_data.keys())
                        rand_ens_cm_scores = processed_data[rand_cm][g][stat]
                    if has_ens_g:
                        rand_g = self.find_rand_bot(list(processed_data[list(processed_data.keys())[0]].keys()))
                        rand_ens_g_scores = processed_data[cm][rand_g][stat]
                    
                    #Now we do the actual figure creation

                    if self.fig:
                        if stat == "Bot Pairing Scores":
                            yl = "CoLT Rating"
                        else:
                            yl = stat

                        data = processed_data[cm][g][stat]
                        x = list(range(1, len(data) + 1))
                        plt.plot(x, data, label="ACE")
                        if has_ens_cm and not has_ens_g and not (best_avg_cm_score == None or best_overall_cm_score_for_g == None):
                            # if self.bot_lm_types.get_bot_lm_type(best_avg_cm) != self.bot_lm_types.get_bot_lm_type(g): plt.axhline(y = best_avg_cm_score, color='r', linestyle=':', label="BA")
                            plt.axhline(y = best_avg_cm_score, color='r', linestyle=':', label="BA")
                            plt.axhline(y = best_overall_cm_score_for_g, color='r', linestyle='solid', label="B")
                        if has_ens_g and not has_ens_cm and not (best_avg_g_score == None or best_overall_g_score_for_cm == None):
                            # if self.bot_lm_types.get_bot_lm_type(best_avg_g) != self.bot_lm_types.get_bot_lm_type(cm): plt.axhline(y = best_avg_g_score, color='r', linestyle=':', label="BA")
                            plt.axhline(y = best_avg_g_score, color='r', linestyle=':', label="BA")
                            plt.axhline(y = best_overall_g_score_for_cm, color='r', linestyle='solid', label="B")
                        if has_ens_cm and rand_ens_cm_scores != None:
                            plt.plot(x, rand_ens_cm_scores, color='c', linestyle='solid', label="R")
                        if has_ens_g and not has_ens_cm and rand_ens_g_scores != None:
                            plt.plot(x, rand_ens_g_scores, color='c', linestyle='solid', label="R")
                        elif has_ens_g and rand_ens_g_scores != None :
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

                    add_files = False
                    if self.conversion[stat] in self.compiled_data_stats:
                        self.populate_needed_fields(self.compiled_data, [cm, g, compile_key])
                        self.compiled_data[cm][g][compile_key][self.conversion[stat]] = []
                        add_files = True

                    for fp in fps:
                        fp += "_" + cm + "+" + g + ".jpg"
                        self.create_path(fp)
                        if self.fig: plt.savefig(fp)
                        if add_files: self.compiled_data[cm][g][compile_key][self.conversion[stat]].append(fp)
                    if self.fig: plt.clf()

                    if has_ens_g: del fps[-1]

    def create_performance_progression_sliding_window_figures(self, processed_data, lp, performance_stats):

        self.create_progression_plots(processed_data, lp, performance_stats, self.file_paths_obj.performance_progression_sliding_window_filepaths, self.performance_progression_sliding_window_stat_keys, self.compiled_data_keys.PERF_PROG_SLIDE)

    def create_performance_progression_figures(self, processed_data, lp, performance_stats):

        self.create_progression_plots(processed_data, lp, performance_stats, self.file_paths_obj.performance_progression_filepaths, self.performance_progression_stat_keys, self.compiled_data_keys.PERF_PROG)

    def create_arm_percentage_figures(self, processed_data, lp):
        #determine if there is an ensemble cm 
        #if there is, then grab the arm weights and plot them under arm_weights_filepaths['cm'][lp]
        ens_cm = self.find_ensemble(processed_data.keys())
        if ens_cm != None:
            for g in processed_data[ens_cm]:
                #create a plot for this match up
                path = self.file_paths_obj.percent_selected_filepaths['cm'] + f"{ens_cm}-{g}.jpg"
                percent_selected = processed_data[ens_cm][g][self.stat_dict_keys.CM_LEARN_STATS][self.stats.PERCENTAGE_BOT_CHOSEN]
                if self.fig: self.create_single_arm_percentage_figure(percent_selected, ens_cm, g, path)

                self.populate_needed_fields(self.compiled_data, [ens_cm, g])
                if self.compiled_data_keys.PERCENTAGES not in self.compiled_data[ens_cm][g]:
                    self.compiled_data[ens_cm][g][self.compiled_data_keys.PERCENTAGES] = []
                self.compiled_data[ens_cm][g][self.compiled_data_keys.PERCENTAGES].append(path)

        #determine if there is an ensemble g
        #if there is, then grab the arm weights and plot them under arm_weights_filepaths['g'][lp]
        ens_g = self.find_ensemble(processed_data[list(processed_data.keys())[0]].keys())
        if ens_g != None:
            for cm in processed_data:
                #create a plot for this team
                path = self.file_paths_obj.percent_selected_filepaths['g'] + f"{cm}-{ens_g}.jpg"
                percent_selected = processed_data[cm][ens_g][self.stat_dict_keys.G_LEARN_STATS][self.stats.PERCENTAGE_BOT_CHOSEN]
                if self.fig: self.create_single_arm_percentage_figure(percent_selected, cm, ens_g, path)

                self.populate_needed_fields(self.compiled_data, [cm, ens_g])
                if self.compiled_data_keys.PERCENTAGES not in self.compiled_data[cm][ens_g]:
                    self.compiled_data[cm][ens_g][self.compiled_data_keys.PERCENTAGES] = []
                self.compiled_data[cm][ens_g][self.compiled_data_keys.PERCENTAGES].append(path)

    def create_single_arm_percentage_figure(self, arm_percentages, cm, g, save_path):
        x_axis = []
        y_axis = []
        for arm in arm_percentages:
            x_axis.append(arm)
            y_axis.append(arm_percentages[arm])
        title = f"arm percentages with\n{cm} and\n{g}"
        x_label = "bots"
        y_label = "percentage"
        if self.fig: self.graph_bar_chart(x_axis, y_axis, title, x_label, y_label, save_path)


    def graph_bar_chart(self, x_axis, y_axis, title, x_label, y_label, save_file):
        # fig, ax = plt.subplots() #layout="constrained"
        
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

        plt.bar(new_x, y_axis)
        plt.xticks(rotation = -45, fontsize = 10)
        self.create_path(save_file)
        plt.savefig(save_file)
        plt.clf() 


    def graph_histogram(self, data, title, x_label, y_label, s_path):
        fig, ax = plt.subplots()
        ax.hist(data, bins=8, alpha=.5, color='b')
        # plt.title(title)
        # plt.ylabel(y_label)
        # plt.xlabel(x_label)
        plt.savefig(s_path)
        plt.clf() 
        plt.close()

    def create_arm_weights_figures(self, processed_data, lp):
        #determine if there is an ensemble cm 
        #if there is, then grab the percent selected and plot them under arm_weights_filepaths['cm']['g'][lp]
        ens_cm = self.find_ensemble(processed_data.keys())
        if ens_cm != None:
            for g in processed_data[ens_cm]:
                #create a plot for this match up
                path = self.file_paths_obj.arm_weights_filepaths['cm'] + f"-{ens_cm}-{g}.jpg"
                arm_weights = processed_data[ens_cm][g][self.stat_dict_keys.CM_LEARN_STATS][self.stats.ARM_WEIGHTS_BY_GAME]
                if self.fig: self.create_single_arm_weights_figure(arm_weights, ens_cm, g, path)

                self.populate_needed_fields(self.compiled_data, [ens_cm, g])
                if self.compiled_data_keys.ARM_WEIGHTS not in self.compiled_data[ens_cm][g]:
                    self.compiled_data[ens_cm][g][self.compiled_data_keys.ARM_WEIGHTS] = []
                self.compiled_data[ens_cm][g][self.compiled_data_keys.ARM_WEIGHTS].append(path)

        #determine if there is an ensemble g
        #if there is, then grab the percent selected and plot them under arm_weights_filepaths['g'][lp]
        ens_g = self.find_ensemble(processed_data[list(processed_data.keys())[0]].keys())
        if ens_g != None:
            for cm in processed_data:
                #create a plot for this team
                path = self.file_paths_obj.arm_weights_filepaths['g'] + f"-{cm}-{ens_g}.jpg"
                arm_weights = processed_data[cm][ens_g][self.stat_dict_keys.G_LEARN_STATS][self.stats.ARM_WEIGHTS_BY_GAME]
                if self.fig: self.create_single_arm_weights_figure(arm_weights, cm, ens_g, path)

                self.populate_needed_fields(self.compiled_data, [cm, ens_g])
                if self.compiled_data_keys.ARM_WEIGHTS not in self.compiled_data[cm][ens_g]:
                    self.compiled_data[cm][ens_g][self.compiled_data_keys.ARM_WEIGHTS] = []
                self.compiled_data[cm][ens_g][self.compiled_data_keys.ARM_WEIGHTS].append(path)

    def create_param_vs_score_figures(self, processed_data):
        #each key in processed data prepresents a different parameter (e.g. 0 = 0, 1 = .001, etc.)
        parameters = self.experiment_settings.independent_variable 

        def create_fig(data, save_path):
            x = parameters
            y = data 
            plt.plot(x, y)
            self.create_path(save_path)
            plt.savefig(save_path)
            plt.clf()
        
        cms = [e for e in list(processed_data.keys()) if e != "avg"]
        gs = list(processed_data[cms[0]].keys())
        for cm in cms:
            for g in gs:
                for stat in processed_data[cm][g]:
                    save_path = self.file_paths_obj.param_comparison_fig_filepaths[cm][g][stat]
                    data = processed_data[cm][g][stat]
                    create_fig(data, save_path)
        
        for stat in processed_data['avg']:
            save_path = self.file_paths_obj.param_comparison_fig_filepaths['avg'][stat]
            data = processed_data['avg'][stat]
            create_fig(data, save_path)
        


    
    def create_single_arm_weights_figure(self, arm_weights, cm, g, save_path):
        for tm in arm_weights:
            tm_weights = arm_weights[tm]
            x_axis = list(range(len(tm_weights)))
            #replace occurrances of inf with 4
            tm_weights = [4.0 if w == np.inf else w for w in tm_weights]
            plt.plot(x_axis, tm_weights, label=tm)
        plt.legend()
        self.create_path(save_path)
        plt.savefig(save_path)
        plt.clf()

    def create_final_arm_perc_fig(self, arm_percentages, save_path):
            x_axis = []
            y_axis = []
            for arm in arm_percentages:
                x_axis.append(arm)
                y_axis.append(arm_percentages[arm])
            if self.fig: self.graph_bar_chart(x_axis, y_axis, None, None, None, save_path)


    def get_final_dist_fig_paths(self, cm, g, new_stat):
        
        btypes = []

        if self.check_if_ensemble(cm) or self.is_rand_ens(cm):
            btypes.append("cm")
        
        if self.check_if_ensemble(g) or self.is_rand_ens(g):
            btypes.append("g")

        fps = []

        for b in btypes:
            dir_path, filename = os.path.split(self.file_paths_obj.final_stat_distribution_filepaths[b])
            filename += f".{cm}+{g}.jpg"
            save_path = os.path.join(dir_path, new_stat, filename)
            self.create_path(save_path)
            fps.append(save_path)
        return fps


    def create_final_distribution_figures(self, processed_data, lp):
        #Create the final arm weights distribution 
        for cm in processed_data:
            for g in processed_data[cm]:
                for s in self.final_stat_dist_keys:
                    if type(s) == list and s[0] in processed_data[cm][g]:
                        new_stat = self.stats.FINAL_STAT_DIST + " ~ " + s[1]
                        arm_percentages = processed_data[cm][g][s[0]][new_stat]
                        #check the bot types 
                        fps = self.get_final_dist_fig_paths(cm, g, new_stat)

                        if self.fig:
                            for save_path in fps:
                                self.create_final_arm_perc_fig(arm_percentages, save_path)

                        #now add the correct filepaths to the compiled data 
                        
                        self.populate_needed_fields(self.compiled_data, [cm, g, self.compiled_data_keys.FINAL_STAT_DIST])
                        self.compiled_data[cm][g][self.compiled_data_keys.FINAL_STAT_DIST][new_stat] = fps


                    elif type(s) != list:
                        new_stat = self.stats.FINAL_STAT_DIST + " ~ " + s
                        final_stat_distribution = processed_data[cm][g][new_stat]

                        fps = self.get_final_dist_fig_paths(cm, g, new_stat)

                        if self.fig:
                            self.graph_histogram(final_stat_distribution, None, None, None, fps[0])
                        
                        if s in self.compiled_data_stats:
                            self.populate_needed_fields(self.compiled_data, [cm, g, self.compiled_data_keys.FINAL_STAT_DIST])
                            self.compiled_data[cm][g][self.compiled_data_keys.FINAL_STAT_DIST][new_stat] = fps[0]
        