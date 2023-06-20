'''
This file creates files based off of the input hyper parameters. It acts like a hashing function by creating the same file name when the same hyperparameters are selected
but all of the names are unique with each change in a hyperparameter. 
This allows us to keep experiments separate and identifiable. 
This file is also in charge of deleting files that already exist when an experiment is run again. (we might re-run experiments for bug fixes and what not)
It loads the needed filepaths into the file_paths_obj and opens the needed files  and holds/opens/closes the actual file objects
'''

from os.path import exists
from os import remove
import os


class FileManager:
    
    def __init__(self, experiment_settings, ai_types, file_paths_obj, bot_ai_types, experiment_types, file_name_directory_elements, parameter_types, performance_progression_stat_keys, performance_progression_sliding_window_stat_keys, main_stat_keys):
        self.experiment_settings = experiment_settings
        self.ai_types = ai_types
        self.file_paths_obj = file_paths_obj
        self.bot_ai_types = bot_ai_types
        self.experiment_types = experiment_types
        self.file_name_directory_elements = file_name_directory_elements
        self.parameter_types = parameter_types
        self.performance_progression_stat_keys = performance_progression_stat_keys
        self.performance_progression_sliding_window_stat_keys = performance_progression_sliding_window_stat_keys
        self.main_stat_keys = main_stat_keys

    #These are the actual file variables that are opened and closed throughout the program
    ROUND_LOG_FILE = None
    LEARN_LOG_FILE_CM = None
    LEARN_LOG_FILE_G = None


    '''
    file_paths_obj already contains all of the needed paths 
    '''
    def generate_needed_filepaths(self):
        #Each filepath has the same root no matter the type of file that it is. 

         #We want to keep the ai_types for cm and g separate because we want to know which one, or if both, contain an ensemble bot
        cm_ai_types, g_ai_types = self.get_bot_types()

        #first task is to set the directory paths for the files
        self.set_directory_paths()

        #second task is to determine the root file name to include in all filepaths
        root_name = self.determine_root_file_name(cm_ai_types, g_ai_types)

        #third task is to create the full filenames and paths
        self.combine_components(root_name, cm_ai_types, g_ai_types)

    #This function takes the number of iterations from settings into account to create all of the needed
    #filepaths for the experiment. If it is just a tournament, all the filepath arrays will only have one
    #element. 
    def combine_components(self, root_name, cm_ai_types, g_ai_types):

        if self.experiment_settings.experiment_type == self.experiment_types.LEARNING_EXPERIMENT:

            self.combine_learn_experiment_comps(root_name, cm_ai_types, g_ai_types)


        elif self.experiment_settings.experiment_type == self.experiment_types.PARAMETER_EXPERIMENT:

            self.combine_param_experiment_comps(root_name)

        else:
            self.set_common_files(root_name, "")
    
    def combine_learn_experiment_comps(self, root_name, cm_ai_types, g_ai_types):
        contains_ensemble_cm = False
        contains_ensemble_g = False

        #If there are ensemble bots then we need to instantiate those filepaths
        if self.ai_types.DISTANCE_ENSEMBLE in cm_ai_types:
            contains_ensemble_cm = True
        if self.ai_types.DISTANCE_ENSEMBLE in g_ai_types:
            contains_ensemble_g = True
        
        name_elements = self.file_name_directory_elements
        name = root_name

        lower = self.experiment_settings.iteration_range[0]
        upper = self.experiment_settings.iteration_range[1]

        #We take care of naming the files that summarize the individual ones
        itr_range = f"{lower}-{upper}"

        #learning experiment
        if contains_ensemble_cm:
            #learn experiment file names
            #directory information has already been appended here
            dir = self.file_paths_obj.learn_experiment_analyses_dir_path
            this_name = name_elements.LEARN_EXPERIMENT_ANALYSIS_PREFIX + name_elements.CODEMASTER_PREFIX + name + itr_range + \
                name_elements.LEARN_EXPERIMENT_ANALYSIS_FILE_TYPE
            self.file_paths_obj.learn_experiment_analysis_filepath_cm = os.path.join(dir, this_name)
            
        if contains_ensemble_g:
            dir = self.file_paths_obj.learn_experiment_analyses_dir_path
            this_name = name_elements.LEARN_EXPERIMENT_ANALYSIS_PREFIX + name_elements.GUESSER_PREFIX + name + itr_range + \
                name_elements.LEARN_EXPERIMENT_ANALYSIS_FILE_TYPE
            self.file_paths_obj.learn_experiment_analysis_filepath_g = os.path.join(dir, this_name)

        #name experiment specific supporting files here
        #Don't worry about naming figure files yet becuase those are just intermediary
        #add names to an array so that we can do the naming of the files that all experiment types have together
        for i in range(lower, upper):
            #We take care of naming the individual iteration files

            #learn period analysis files
            if contains_ensemble_cm:
                dir = self.file_paths_obj.learn_period_analyses_dir_path
                this_name = name_elements.LEARN_PERIOD_ANALYSIS_PREFIX + name_elements.CODEMASTER_PREFIX + name + \
                    "_" + str(i) + name_elements.LEARN_PERIOD_ANALYSIS_FILE_TYPE 
                self.file_paths_obj.learn_period_analysis_filepaths_cm.append(os.path.join(dir, this_name))

                #learn logs
                dir = self.file_paths_obj.learn_logs_dir_path
                this_name = name_elements.LEARN_LOG_PREFIX + name_elements.CODEMASTER_PREFIX + name + "_" + str(i) + name_elements.LEARN_LOG_FILE_TYPE
                self.file_paths_obj.learn_log_filepaths_cm.append(os.path.join(dir, this_name))

                #learn tables
                dir = self.file_paths_obj.learn_tables_dir_path
                this_name = name_elements.LEARN_TABLE_PREFIX + name_elements.CODEMASTER_PREFIX + name + "_" + str(i) + name_elements.LEARN_TABLE_FILE_TYPE
                self.file_paths_obj.learn_table_filepaths.append(os.path.join(dir, this_name))

                #learn figures
                self.create_learn_fig_paths(name, name_elements.CODEMASTER_PREFIX, i)

            if contains_ensemble_g:
                dir = self.file_paths_obj.learn_period_analyses_dir_path
                this_name = name_elements.LEARN_PERIOD_ANALYSIS_PREFIX + name_elements.GUESSER_PREFIX + name + \
                    "_" + str(i) + name_elements.LEARN_PERIOD_ANALYSIS_FILE_TYPE
                self.file_paths_obj.learn_period_analysis_filepaths_g.append(os.path.join(dir, this_name))

                #learn logs
                dir = self.file_paths_obj.learn_logs_dir_path
                this_name = name_elements.LEARN_LOG_PREFIX + name_elements.GUESSER_PREFIX + name + "_" + str(i) + name_elements.LEARN_LOG_FILE_TYPE
                self.file_paths_obj.learn_log_filepaths_g.append(os.path.join(dir, this_name))

                #learn tables
                dir = self.file_paths_obj.learn_tables_dir_path
                this_name = name_elements.LEARN_TABLE_PREFIX + name_elements.GUESSER_PREFIX + name + "_" + str(i) + name_elements.LEARN_TABLE_FILE_TYPE
                self.file_paths_obj.learn_table_filepaths.append(os.path.join(dir, this_name))

                #learn figures
                self.create_learn_fig_paths(name, name_elements.GUESSER_PREFIX, i)
                    
            self.set_common_files(name, i)
        
        #We add one more processed data file and learn table file because we will be combining all of the components 
        #We do this only for learning experiments because it is the only type of experiment that needs 
        #averages across many tournaments
        dir = self.file_paths_obj.processed_data_dir_path
        this_name = name_elements.PROCESSED_DATA_PREFIX + name + "_final" + name_elements.PROCESSED_DATA_FILE_TYPE
        self.file_paths_obj.processed_data_filepaths.append(os.path.join(dir, this_name))

        dir = self.file_paths_obj.learn_tables_dir_path
        this_name = name_elements.LEARN_TABLE_PREFIX + name + "_final" + name_elements.LEARN_TABLE_FILE_TYPE
        self.file_paths_obj.learn_table_filepaths.append(os.path.join(dir, this_name))


        #Create learning figures for the final (averaged) data
        if contains_ensemble_cm:
            self.create_learn_fig_paths(name, name_elements.CODEMASTER_PREFIX, "_final")
        if contains_ensemble_g:
            self.create_learn_fig_paths(name, name_elements.GUESSER_PREFIX, "_final")

    def combine_param_experiment_comps(self, root_name):
            #The parameter that is being changed will be specified in the experiment name
            parameters = self.experiment_settings.independent_variable

            lower = parameters[0]
            upper = parameters[-1]
            param_range = f"{lower}-{upper}"

            name_elements = self.file_name_directory_elements

            #For every pair (and average of all pairs) and every stat, we want a different figure
            for stat in self.main_stat_keys:
                for cm in self.experiment_settings.codemasters:
                    for g in self.experiment_settings.guessers:

                        if cm not in self.file_paths_obj.param_comparison_fig_filepaths:
                            self.file_paths_obj.param_comparison_fig_filepaths[cm] = {}
                        if g not in self.file_paths_obj.param_comparison_fig_filepaths[cm]:
                            self.file_paths_obj.param_comparison_fig_filepaths[cm][g] = {}


                        fname = name_elements.PARAMETER_COMPARISON_FIGURE_PREFIX + stat + "_" + cm + "-" + g + "_" + \
                              root_name + param_range + name_elements.PARAMETER_COMPARISON_FIGURE_FILE_TYPE
                        dir = self.file_paths_obj.param_comparison_figs_dir_path

                        self.file_paths_obj.param_comparison_fig_filepaths[cm][g][stat] = os.path.join(dir, stat, fname)
                        
                #add the average for all as well
                fname = name_elements.PARAMETER_COMPARISON_FIGURE_PREFIX + stat + "_avg_perf_" + \
                        root_name + param_range + name_elements.PARAMETER_COMPARISON_FIGURE_FILE_TYPE
                dir = self.file_paths_obj.param_comparison_figs_dir_path

                if "avg" not in self.file_paths_obj.param_comparison_fig_filepaths:
                    self.file_paths_obj.param_comparison_fig_filepaths['avg'] = {}
                self.file_paths_obj.param_comparison_fig_filepaths["avg"][stat] = os.path.join(dir, stat, fname)
            
            for p in parameters:
                self.set_common_files(root_name, str(p))



    
    def create_learn_fig_paths(self, name, type_prefix, itr_suffix):
        name_elements = self.file_name_directory_elements
        b_type = type_prefix[:-1]

        #set the type prefix in all of the filepath dictionaries
        if b_type not in self.file_paths_obj.performance_progression_filepaths:
            self.file_paths_obj.performance_progression_filepaths[b_type] = {}
            self.file_paths_obj.performance_progression_sliding_window_filepaths[b_type] = {}
        

        if b_type not in self.file_paths_obj.percent_selected_filepaths:
            #arm percentage figures
            dir = self.file_paths_obj.percent_selected_dir_path
            this_name = name_elements.ARM_PERCENTAGE_PREFIX + type_prefix + name + str(itr_suffix)
            self.file_paths_obj.percent_selected_filepaths[b_type] = os.path.join(dir, this_name)
        
        if b_type not in self.file_paths_obj.arm_weights_filepaths:
            #arm weights figures
            dir = self.file_paths_obj.arm_weights_dir_path
            this_name = name_elements.ARM_WEIGHTS_PREFIX + type_prefix + name + str(itr_suffix)
            self.file_paths_obj.arm_weights_filepaths[b_type] = os.path.join(dir, this_name)
        
        if b_type not in self.file_paths_obj.final_stat_distribution_filepaths:
            dir = self.file_paths_obj.final_stat_distribution_dir_path
            this_name = name_elements.FINAL_STAT_DIST_PREFIX + type_prefix + name + str(itr_suffix)
            self.file_paths_obj.final_stat_distribution_filepaths[b_type] = os.path.join(dir, this_name)

        #performance progression figures (loop through all of the wanted stats for this)
        for stat in self.performance_progression_stat_keys:
            if stat not in self.file_paths_obj.performance_progression_filepaths[b_type]:
                self.file_paths_obj.performance_progression_filepaths[b_type][stat] = []
            dir = os.path.join(self.file_paths_obj.performance_progression_dir_path, stat)
            this_name = name_elements.PERFORMANCE_PROGRESSION_PREFIX + b_type + "_" + stat + "_" + name + str(itr_suffix)
            self.file_paths_obj.performance_progression_filepaths[b_type][stat].append(os.path.join(dir, this_name))
        
        for stat in self.performance_progression_sliding_window_stat_keys:
            if stat not in self.file_paths_obj.performance_progression_filepaths[b_type]:
                self.file_paths_obj.performance_progression_sliding_window_filepaths[b_type][stat] = []
            dir = os.path.join(self.file_paths_obj.performance_progression_sliding_window_dir_path, stat)
            this_name = name_elements.PERFORMANCE_PROGRESSION_SLIDING_WINDOW_PREFIX + b_type + "_" + stat + "_" + name + str(itr_suffix)
            self.file_paths_obj.performance_progression_sliding_window_filepaths[b_type][stat].append(os.path.join(dir, this_name))



    def set_common_files_param(self, name, val, d):

        name_elements = self.file_name_directory_elements

        #round logs
        dir = self.file_paths_obj.round_logs_dir_path
        this_name = name_elements.ROUND_LOG_PREFIX + name + "_" + str(val) + name_elements.ROUND_LOG_FILE_TYPE
        self.file_paths_obj.round_log_filepaths.append(os.path.join(dir, this_name))

        #parsed data
        dir = self.file_paths_obj.parsed_data_dir_path
        this_name = name_elements.PARSED_DATA_PREFIX + name + "_" + str(val) + name_elements.PARSED_DATA_FILE_TYPE
        self.file_paths_obj.parsed_data_filepaths.append(os.path.join(dir, this_name))

        #processed data
        dir = self.file_paths_obj.processed_data_dir_path
        this_name = name_elements.PROCESSED_DATA_PREFIX + name + "_" + str(val) + name_elements.PROCESSED_DATA_FILE_TYPE
        self.file_paths_obj.processed_data_filepaths.append(os.path.join(dir, this_name))

        #tournament table name
        dir = self.file_paths_obj.tournament_tables_dir_path
        this_name = name_elements.TOURNAMENT_TABLE_PREFIX + name + "_" + str(val) + name_elements.TOURNAMENT_TABLE_FILE_TYPE
        self.file_paths_obj.tournament_table_filepaths.append(os.path.join(dir, this_name))

        

    def set_common_files(self, name, val):

        name_elements = self.file_name_directory_elements

        #round logs
        dir = self.file_paths_obj.round_logs_dir_path
        this_name = name_elements.ROUND_LOG_PREFIX + name + "_" + str(val) + name_elements.ROUND_LOG_FILE_TYPE
        self.file_paths_obj.round_log_filepaths.append(os.path.join(dir, this_name))

        #parsed data
        dir = self.file_paths_obj.parsed_data_dir_path
        this_name = name_elements.PARSED_DATA_PREFIX + name + "_" + str(val) + name_elements.PARSED_DATA_FILE_TYPE
        self.file_paths_obj.parsed_data_filepaths.append(os.path.join(dir, this_name))

        #processed data
        dir = self.file_paths_obj.processed_data_dir_path
        this_name = name_elements.PROCESSED_DATA_PREFIX + name + "_" + str(val) + name_elements.PROCESSED_DATA_FILE_TYPE
        self.file_paths_obj.processed_data_filepaths.append(os.path.join(dir, this_name))

        #tournament table name
        dir = self.file_paths_obj.tournament_tables_dir_path
        this_name = name_elements.TOURNAMENT_TABLE_PREFIX + name + "_" + str(val) + name_elements.TOURNAMENT_TABLE_FILE_TYPE
        self.file_paths_obj.tournament_table_filepaths.append(os.path.join(dir, this_name))


    def get_experiment_specific_root(self, root_file_name):

        #now we check if it is a learning experiment (if it was a parameter experiment, the parameters will have been changed above already)
        if self.experiment_settings.experiment_type == self.experiment_types.LEARNING_EXPERIMENT:
            #check if it has the underlying lm
            if self.experiment_settings.include_same_lm:
                root_file_name += self.file_name_directory_elements.WITH_LM
            else:
                root_file_name += self.file_name_directory_elements.WITHOUT_LM
            #append the ensemble parameters
            for i in range(len(self.experiment_settings.ensemble_parameters)):
                root_file_name += f"_p{i}.{self.experiment_settings.ensemble_parameters[i]}"

            root_file_name += self.file_name_directory_elements.LEARN_PERIOD_ITERATIONS_PREFIX

        elif self.experiment_settings.experiment_type == self.experiment_types.PARAMETER_EXPERIMENT:
            root_file_name += self.file_name_directory_elements.IND_VAR_VAL

        #Otherwise, we are running a tournament and we don't need additional info in the file name

        return root_file_name


    def get_bot_types(self):
        #Loop through all the guessers and codemasters and determine the AIType
        #These are hashsets (constant time lookup)
        cm_ai_types = set()
        g_ai_types = set()
        for cm in self.experiment_settings.codemasters:
            ai_type = self.bot_ai_types.get_bot_ai_type(cm)
            cm_ai_types.add(ai_type)
        for g in self.experiment_settings.guessers:
            ai_type = self.bot_ai_types.get_bot_ai_type(g)
            g_ai_types.add(ai_type)
        
        return cm_ai_types, g_ai_types

    def determine_root_file_name(self, cm_ai_types, g_ai_types):
        if self.experiment_settings.custom_root_name == None:
            #Every file needs to contain the number of games run between each bot pairing and the experiment name. The hyper parameters 
            # will only be included for the type of bots in the tournament
            root_file_name = self.experiment_settings.config_setting + "." + self.experiment_settings.tournament_setting + self.file_name_directory_elements.N_GAMES_PREFIX + str(self.experiment_settings.n_games) + \
                self.file_name_directory_elements.B_SIZE_PREFIX + str(self.experiment_settings.board_size)

            root_file_name = self.get_experiment_specific_root(root_file_name)

        else:
            root_file_name = self.experiment_settings.custom_root_name

        
        return root_file_name
    
    def set_directory_paths(self):
        #We need to generate the parts of the paths that will be used among all paths
        root_path = os.path.join(self.file_paths_obj.results_root, "saved_results")

        #we need to see what type of experiment this is so we can deptermine the paths
        name_elements = self.file_name_directory_elements
        if self.experiment_settings.experiment_type == self.experiment_types.LEARNING_EXPERIMENT:
            root_path = os.path.join(root_path, name_elements.LEARNING_EXPERIMENTS_DIR)

            self.file_paths_obj.learn_figs_dir_path = os.path.join(root_path, name_elements.VISUALIZATIONS_DIR, \
                name_elements.FIGURES_DIR, name_elements.LEARN_FIGS_DIR)

            self.file_paths_obj.performance_progression_dir_path = os.path.join(root_path, name_elements.VISUALIZATIONS_DIR, \
                name_elements.FIGURES_DIR, name_elements.LEARN_FIGS_DIR, name_elements.PERF_PROG_DIR)
            self.file_paths_obj.performance_progression_sliding_window_dir_path = os.path.join(root_path, name_elements.VISUALIZATIONS_DIR, \
                name_elements.FIGURES_DIR, name_elements.LEARN_FIGS_DIR, name_elements.PERF_PROG_SLIDE_WIND_DIR)
            self.file_paths_obj.arm_weights_dir_path = os.path.join(root_path, name_elements.VISUALIZATIONS_DIR, \
                name_elements.FIGURES_DIR, name_elements.LEARN_FIGS_DIR, name_elements.ARM_WEIGHTS_DIR)
            self.file_paths_obj.percent_selected_dir_path = os.path.join(root_path, name_elements.VISUALIZATIONS_DIR, \
                name_elements.FIGURES_DIR, name_elements.LEARN_FIGS_DIR, name_elements.PERC_SELECTED_DIR)  
            self.file_paths_obj.final_stat_distribution_dir_path = os.path.join(root_path, name_elements.VISUALIZATIONS_DIR, \
                name_elements.FIGURES_DIR, name_elements.LEARN_FIGS_DIR, name_elements.FINAL_STAT_DIST_DIR)
            
            self.file_paths_obj.learn_period_analyses_dir_path = os.path.join(root_path, \
                name_elements.LEARN_PERIOD_ANALYSES_DIR)
            self.file_paths_obj.learn_logs_dir_path = os.path.join(root_path, name_elements.RAW_DATA_DIR, \
                name_elements.LEARN_LOGS_DIR)
            self.file_paths_obj.learn_tables_dir_path = os.path.join(root_path, name_elements.VISUALIZATIONS_DIR, \
                name_elements.TABLES_DIR, name_elements.LEARN_TABLES_DIR)

            self.file_paths_obj.learn_experiment_analyses_dir_path = os.path.join(root_path, \
                name_elements.LEARN_EXPERIMENT_ANALYSES_DIR)
        elif self.experiment_settings.experiment_type == self.experiment_types.PARAMETER_EXPERIMENT:
            root_path = os.path.join(root_path, name_elements.PARAMETER_EXPERIMENTS_DIR)

            self.file_paths_obj.param_comparison_figs_dir_path = os.path.join(root_path, name_elements.VISUALIZATIONS_DIR, \
                name_elements.FIGURES_DIR, name_elements.PARAM_COMPARISON_FIGS_DIR)
            #This is set as directory paths because we can just append to the filepath
            #there are is at most one per experiment. 
            self.file_paths_obj.param_experiment_analysis_filepath = os.path.join(root_path, \
                name_elements.PARAM_EXPERIMENT_ANALYSES_DIR)
        else:
            #its a tournament
            root_path = os.path.join(root_path, name_elements.TOURNAMENTS_DIR)

        #now we set the common elements
        self.file_paths_obj.round_logs_dir_path = os.path.join(root_path, name_elements.RAW_DATA_DIR, \
            name_elements.ROUND_LOGS_DIR)
        self.file_paths_obj.parsed_data_dir_path = os.path.join(root_path, name_elements.PARSED_DATA_DIR)
        self.file_paths_obj.processed_data_dir_path = os.path.join(root_path, name_elements.PROCESSED_DATA_DIR)
        self.file_paths_obj.cm_stats_dir_path = os.path.join(root_path, name_elements.VISUALIZATIONS_DIR, \
            name_elements.FIGURES_DIR, name_elements.CM_STATS_DIR)
        self.file_paths_obj.tournament_tables_dir_path = os.path.join(root_path, name_elements.VISUALIZATIONS_DIR, \
            name_elements.TABLES_DIR, name_elements.TOURNAMENT_TABLES_DIR)





    def reset_filepaths(self):
        self.file_paths_obj.score_logs_filepath = self.file_paths_obj.log_root
        self.file_paths_obj.game_logs_filepath = self.file_paths_obj.log_root
        self.file_paths_obj.round_logs_filepath = self.file_paths_obj.log_root
        self.file_paths_obj.table_logs_filepath = self.file_paths_obj.log_root
        self.file_paths_obj.learn_logs_filepath_cm = self.file_paths_obj.log_root
        self.file_paths_obj.learn_logs_filepath_g = self.file_paths_obj.log_root

    def delete_existing(self):
        if exists(self.file_paths_obj.score_logs_filepath):
            remove(self.file_paths_obj.score_logs_filepath)
        if exists(self.file_paths_obj.game_logs_filepath):
            remove(self.file_paths_obj.game_logs_filepath)
        if exists(self.file_paths_obj.round_logs_filepath):
            remove(self.file_paths_obj.round_logs_filepath)
        if exists(self.file_paths_obj.table_logs_filepath):
            remove(self.file_paths_obj.table_logs_filepath) 
        if exists(self.file_paths_obj.parsable_table_stats_filepath):
            remove(self.file_paths_obj.parsable_table_stats_filepath)  