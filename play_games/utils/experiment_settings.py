'''
This file has all of the overarching settings. Many of the files import this file and use these settings. 
It also is in charge of parsing the settings in the config file.

All objects that are shared among files are stored here. I store them here because a lot of the settings get changed at start up and need to 
be kept for all the files. 

'''

import json
import configparser

#TODO: Write checks to make sure that all settings are compatible

class ExperimentSettings:

    def __init__(self, experiment_types, file_paths_obj, config_keys):
        self.experiment_types = experiment_types
        self.file_paths_obj = file_paths_obj
        self.config_keys = config_keys
        self.config = None

        ###---set this here---###

        self.config_setting = "DIST_ASSOC_RAND_ENS_W"

        ###---set these in config file---###

        self.tournament_setting = None 
        self.custom_root_name = None

        #can be parameter experiment or learning experiment
        self.experiment_type = None

        ###--Display-Parameters---###
        self.verbose_flag = None
        self.print_boards = None
        self.print_learning = None

        ###---Experimental Settings---###

        #parameter experiment settings
        self.n_associations = None
        #don't touch this
        self.independent_variable = None

        #Learning experiment settings
        self.learning_algorithm = None
        self.iteration_range = None
        self.include_same_lm = None
        self.ensemble_parameters = None

        self.n_games = None
        self.board_size = None

        self.codemasters = None
        self.guessers = None

        self.setup()

    def get_settings_from_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.file_paths_obj.config_file)

        self.tournament_setting = self.config[self.config_setting][self.config_keys.TOURNAMENT_SETTING]
        self.n_games = int(self.config[self.config_setting][self.config_keys.N_GAMES])
        self.n_associations = json.loads(self.config[self.config_setting][self.config_keys.N_ASSOCIATIONS])
        self.board_size = int(self.config[self.config_setting][self.config_keys.BOARD_SIZE])
        self.custom_root_name = self.config[self.config_setting][self.config_keys.CUSTOM_ROOT_NAME]
        self.learning_algorithm = self.config[self.config_setting][self.config_keys.LEARNING_ALGORITHM]
        self.iteration_range = json.loads(self.config[self.config_setting][self.config_keys.ITERATION_RANGE])
        self.include_same_lm = self.config[self.config_setting][self.config_keys.INCLUDE_SAME_LM]
        # self.ensemble_parameters = json.loads(self.config[self.config_setting][self.config_keys.ENSEMBLE_PARAMETERS])
        self.ensemble_parameters = [.5, 0]
        self.codemasters = json.loads(self.config[self.tournament_setting][self.config_keys.CODEMASTERS])
        self.guessers = json.loads(self.config[self.tournament_setting][self.config_keys.GUESSERS])
        self.experiment_type = self.config[self.config_setting][self.config_keys.EXPERIMENT_TYPE]
        self.verbose_flag = self.config[self.config_setting][self.config_keys.VERBOSE_FLAG]
        self.print_boards = self.config[self.config_setting][self.config_keys.PRINT_BOARDS]
        self.print_learning = self.config[self.config_setting][self.config_keys.PRINT_LEARNING]

    #This function gets the settings from config file, sets them, and makes assumptions from settings
    def setup(self):
        self.get_settings_from_config()

        #We check and convert the needed settings
        if self.experiment_type.lower() == 'none':
            self.experiment_type = None
        elif self.experiment_type != self.experiment_types.PARAMETER_EXPERIMENT and self.experiment_type != self.experiment_types.LEARNING_EXPERIMENT:
            print("incorrect experiment type. Type 'None', 'learning experiment' or 'parameter experiment'.")
            exit(-1)

        if self.custom_root_name == "" or self.custom_root_name.lower() == "none":
            self.custom_root_name = None

        if self.learning_algorithm == "" or self.learning_algorithm.lower() == "none":
            self.learning_algorithm == None

        if self.include_same_lm.lower() == "true":
            self.include_same_lm = True
        elif self.include_same_lm.lower() == "false":
            self.include_same_lm = False
        else:
            print("incorrect value for include_same_lm. Set value as either 'True' or 'False'")
            exit(-1)
        
        if str(self.ensemble_parameters).lower() == "none":
            self.ensemble_parameters = None
        else:
            self.ensemble_parameters = [float(v) for v in self.ensemble_parameters]

        if str(self.n_associations).lower() == "none":
            self.n_associations = None
        else:
            self.n_associations = [int(v) for v in self.n_associations]

        if str(self.iteration_range).lower() == "none":
            self.iteration_range = None
        else:
            self.iteration_range = [int(v) for v in self.iteration_range]

        if self.verbose_flag.lower() == "true":
            self.verbose_flag == True
        elif self.verbose_flag.lower() == "false":
            self.verbose_flag = False
        else:
            print("incorrect value for verbose_flag. Set value as either 'True' or 'False'")
            exit(-1)

        if self.print_boards.lower() == "true":
            self.print_boards == True
        elif self.print_boards.lower() == "false":
            self.print_boards = False
        else:
            print("incorrect value for print_boards. Set value as either 'True' or 'False'")
            exit(-1)

        if self.print_learning.lower() == "true":
            self.print_learning == True
        elif self.print_learning.lower() == "false":
            self.print_learning = False
        else:
            print("incorrect value for print_learning. Set value as either 'True' or 'False'")
            exit(-1)


        if self.experiment_type == self.experiment_types.PARAMETER_EXPERIMENT:
            self.determine_variables()

    def determine_variables(self):
        #Here, we go through all the possible independent variables for an experiment and we find which one it is
        if self.n_associations != None and len(self.n_associations) > 1:
            self.independent_variable = self.n_associations
        elif self.ensemble_parameters != None and len(self.ensemble_parameters) > 0 and type(self.ensemble_parameters) == list and len(self.ensemble_parameters) > 1:
            self.independent_variable = self.ensemble_parameters
        




