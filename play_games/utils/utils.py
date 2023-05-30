class Parameters:
    N_ASSOCIATIONS = "Number of Associations"

def cond_print(msg, VERBOSE_FLAG):
    if VERBOSE_FLAG == 1:
        print(msg)

class BotTypes:
    W2V_GLOVE_BASELINE_GUESSER = 'w2v_glove baseline guesser'
    W2V_BASELINE_GUESSER = "w2v baseline guesser"
    GLOVE_50_BASELINE_GUESSER = "glove 50 baseline guesser"
    GLOVE_100_BASELINE_GUESSER = "glove 100 baseline guesser"
    GLOVE_200_BASELINE_GUESSER = "glove 200 baseline guesser"
    GLOVE_300_BASELINE_GUESSER = "glove 300 baseline guesser"
    CN_NB_BASELINE_GUESSER = "cn_nb baseline guesser"

    W2V_DISTANCE_ASSOCIATOR = "w2v distance associator"
    GLOVE_300_DISTANCE_ASSOCIATOR = "glove 300 distance associator"
    GLOVE_50_DISTANCE_ASSOCIATOR = "glove 50 distance associator"
    GLOVE_100_DISTANCE_ASSOCIATOR = "glove 100 distance associator"
    GLOVE_200_DISTANCE_ASSOCIATOR = "glove 200 distance associator"
    W2V_GLOVE_DISTANCE_ASSOCIATOR = "w2v_glove distance associator"
    CN_NB_DISTANCE_ASSOCIATOR = "cn_nb distance associator"

    DISTANCE_ENSEMBLE_CODEMASTER = "distance ensemble codemaster"
    DISTANCE_ENSEMBLE_GUESSER = "distance ensemble guesser"

    RANDOM_DISTANCE_ENSEMBLE_GUESSER = "random distance ensemble guesser"
    RANDOM_DISTANCE_ENSEMBLE_CODEMASTER= "random distance ensemble codemaster"

class AITypes:
    DISTANCE_ASSOCIATOR = "distance_associator"
    BASELINE = "baseline" 
    DISTANCE_ENSEMBLE = "distance ensemble"
    RANDOM_DISTANCE_ENSEMBLE = "random distance ensemble"

class LMTypes:
    W2V = 0
    W2V_GLOVE_C = 1
    GLOVE_50 = 2
    GLOVE_100 = 3
    GLOVE_200 = 4
    GLOVE_300 = 5
    CN_NB = 6
    W2V_GLOVE_G = 7
    NONE = 12
    ENSEMBLE = 13
    RANDOM_ENSEMBLE = 14

class ConfigKeys:
    N_GAMES = "n_games"
    N_ASSOCIATIONS = "n_associations"
    BOARD_SIZE = "board_size"
    TOURNAMENT_SETTING = "tournament_setting"
    CODEMASTERS = "codemasters"
    GUESSERS = "guessers"
    EXPERIMENT_TYPE = "experiment_type"
    CUSTOM_ROOT_NAME = "custom_root_name"
    LEARNING_ALGORITHM = "learning_algorithm"
    IS_PARAMETER_OPTIMIZATION = "is_parameter_optimization"
    CURR_ITERATION = "curr_iteration"
    ITERATION_RANGE = "iteration_range"
    INCLUDE_SAME_LM = "include_same_lm"
    CONVERGENCE_THRESHOLD = "convergence_threshold"
    ENSEMBLE_PARAMETERS = "ensemble_parameters"
    VERBOSE_FLAG = "verbose_flag"
    PRINT_BOARDS = "print_boards"
    PRINT_LEARNING = "print_learning"

class ExperimentTypes:
    LEARNING_EXPERIMENT = "learning experiment"
    PARAMETER_EXPERIMENT = "parameter experiment"

class BotConstructorTypes:
    VECTOR_BASELINE_CODEMASTER = 1
    ENSEMBLE_AI_CODEMASTER = 3
    DISTANCE_ASSOCIATOR_AI_CODEMASTER = 4
    VECTOR_BASELINE_GUESSER = 7
    ENSEMBLE_AI_GUESSER = 8
    RANDOM_ENSEMBLE_AI_CODEMASTER = 10
    RANDOM_ENSEMBLE_AI_GUESSER = 11 

