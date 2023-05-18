'''
This file has the enumerations that are used throughout the project and a hash map that gives the project a double hash map capability for config incorporation

authors: Spencer Brosnahan
Kyle Rogers wrote the cond_print function
'''

class Parameters:
    N_ASSOCIATIONS = "Number of Associations"

def cond_print(msg, VERBOSE_FLAG):
    if VERBOSE_FLAG == 1:
        print(msg)

class BotTypes:
    
    BERT_ASSOCIATOR_CODEMASTER = 'bert associator codemaster'
    HUMAN_ASSOCIATOR_CODEMASTER = "human associator codemaster"
    CONCEPTNET_ASSOCIATOR_CODEMASTER = "conceptnet associator codemaster"
    T5_ASSOCIATOR_CODEMASTER = 't5 associator codemaster'
    GLOVE_ASSOCIATOR_CODEMASTER = 'glove associator codemaster'
    W2V_ASSOCIATOR_CODEMASTER = 'w2v associator codemaster'

    BERT_ASSOCIATOR_GUESSER = 'bert associator guesser'
    HUMAN_ASSOCIATOR_GUESSER = 'human associator guesser'
    CONCEPTNET_ASSOCIATOR_GUESSER = 'conceptnet associator guesser'
    T5_ASSOCIATOR_GUESSER = 't5 associator guesser'
    GLOVE_ASSOCIATOR_GUESSER = 'glove associator guesser'
    W2V_ASSOCIATOR_GUESSER = 'w2v associator guesser'

    BERT_EXT_ASSOCIATOR_CODEMASTER = "bert expanded associator codemaster"
    HUMAN_EXT_ASSOCIATOR_CODEMASTER = "human expanded associator codemaster"
    CONCEPTNET_EXT_ASSOCIATOR_CODEMASTER = "conceptnet expanded associator codemaster"
    T5_EXT_ASSOCIATOR_CODEMASTER = "t5 expanded associator codemaster"

    BERT_EXT_ASSOCIATOR_GUESSER = "bert expanded associator guesser"
    HUMAN_EXT_ASSOCIATOR_GUESSER = "human expanded associator guesser"
    CONCEPTNET_EXT_ASSOCIATOR_GUESSER = "conceptnet expanded associator guesser"
    T5_EXT_ASSOCIATOR_GUESSER = "t5 expanded associator guesser"

    W2V_GLOVE_BASELINE_CODEMASTER_03 = 'w2v_glove baseline codemaster 03'
    W2V_GLOVE_BASELINE_CODEMASTER_05 = 'w2v_glove baseline codemaster 05'
    W2V_GLOVE_BASELINE_CODEMASTER_07 = 'w2v_glove baseline codemaster 07'

    W2V_GLOVE_BASELINE_GUESSER = 'w2v_glove baseline guesser'

    W2V_BASELINE_CODEMASTER_03 = "w2v baseline codemaster 03"
    W2V_BASELINE_CODEMASTER_05 = "w2v baseline codemaster 05"
    W2V_BASELINE_CODEMASTER_07 = "w2v baseline codemaster 07"

    GLOVE_50_BASELINE_CODEMASTER_03 = "glove 50 baseline codemaster 03"
    GLOVE_50_BASELINE_CODEMASTER_05 = "glove 50 baseline codemaster 05"
    GLOVE_50_BASELINE_CODEMASTER_07 = "glove 50 baseline codemaster 07"

    GLOVE_100_BASELINE_CODEMASTER_03 = "glove 100 baseline codemaster 03"
    GLOVE_100_BASELINE_CODEMASTER_05 = "glove 100 baseline codemaster 05"
    GLOVE_100_BASELINE_CODEMASTER_07 = "glove 100 baseline codemaster 07"

    GLOVE_200_BASELINE_CODEMASTER_03 = "glove 200 baseline codemaster 03"
    GLOVE_200_BASELINE_CODEMASTER_05 = "glove 200 baseline codemaster 05"
    GLOVE_200_BASELINE_CODEMASTER_07 = "glove 200 baseline codemaster 07"

    GLOVE_300_BASELINE_CODEMASTER_03 = "glove 300 baseline codemaster 03"
    GLOVE_300_BASELINE_CODEMASTER_05 = "glove 300 baseline codemaster 05"
    GLOVE_300_BASELINE_CODEMASTER_07 = "glove 300 baseline codemaster 07"

    W2V_BASELINE_GUESSER = "w2v baseline guesser"
    GLOVE_50_BASELINE_GUESSER = "glove 50 baseline guesser"
    GLOVE_100_BASELINE_GUESSER = "glove 100 baseline guesser"
    GLOVE_200_BASELINE_GUESSER = "glove 200 baseline guesser"
    GLOVE_300_BASELINE_GUESSER = "glove 300 baseline guesser"
    CN_NB_BASELINE_GUESSER = "cn_nb baseline guesser"

    BERT_UNDIRECTED_GRAPH_GUESSER = "bert undirected graph guesser"
    CONCEPTNET_UNDIRECTED_GRAPH_GUESSER = "conceptnet undirected graph guesser"
    GLOVE_UNDIRECTED_GRAPH_GUESSER = "glove undirected graph guesser"
    HUMAN_UNDIRECTED_GRAPH_GUESSER = "human undirected graph guesser"
    T5_UNDIRECTED_GRAPH_GUESSER = "t5 undirected graph guesser"
    W2V_UNDIRECTED_GRAPH_GUESSER = "w2v undirected graph guesser"

    BERT_UNDIRECTED_WORD_GRAPH_GUESSER = "bert undirected word graph guesser"
    CONCEPTNET_UNDIRECTED_WORD_GRAPH_GUESSER = "conceptnet undirected word graph guesser"
    GLOVE_UNDIRECTED_WORD_GRAPH_GUESSER = "glove undirected word graph guesser"
    HUMAN_UNDIRECTED_WORD_GRAPH_GUESSER = "human undirected word graph guesser"
    T5_UNDIRECTED_WORD_GRAPH_GUESSER = "t5 undirected word graph guesser"
    W2V_UNDIRECTED_WORD_GRAPH_GUESSER = "w2v undirected word graph guesser"

    BERT_UNDIRECTED_WORD_GRAPH_CODEMASTER = "bert undirected word graph codemaster"
    CONCEPTNET_UNDIRECTED_WORD_GRAPH_CODEMASTER = "conceptnet undirected word graph codemaster"
    GLOVE_UNDIRECTED_WORD_GRAPH_CODEMASTER = "glove undirected word graph codemaster"
    HUMAN_UNDIRECTED_WORD_GRAPH_CODEMASTER = "human undirected word graph codemaster"
    T5_UNDIRECTED_WORD_GRAPH_CODEMASTER = "t5 undirected word graph codemaster"
    W2V_UNDIRECTED_WORD_GRAPH_CODEMASTER = "w2v undirected word graph codemaster"

    OPTIMIZED_W2V_GLOVE_BASELINE_CODEMASTER_03 = 'optimized w2v_glove baseline codemaster 03'
    OPTIMIZED_W2V_GLOVE_BASELINE_CODEMASTER_05 = 'optimized w2v_glove baseline codemaster 05'
    OPTIMIZED_W2V_GLOVE_BASELINE_CODEMASTER_07 = 'optimized w2v_glove baseline codemaster 07'

    OPTIMIZED_W2V_BASELINE_CODEMASTER_03 = "optimized w2v baseline codemaster 03"
    OPTIMIZED_W2V_BASELINE_CODEMASTER_05 = "optimized w2v baseline codemaster 05"
    OPTIMIZED_W2V_BASELINE_CODEMASTER_07 = "optimized w2v baseline codemaster 07"

    OPTIMIZED_GLOVE_50_BASELINE_CODEMASTER_03 = "optimized glove 50 baseline codemaster 03"
    OPTIMIZED_GLOVE_50_BASELINE_CODEMASTER_05 = "optimized glove 50 baseline codemaster 05"
    OPTIMIZED_GLOVE_50_BASELINE_CODEMASTER_07 = "optimized glove 50 baseline codemaster 07"

    OPTIMIZED_GLOVE_100_BASELINE_CODEMASTER_03 = "optimized glove 100 baseline codemaster 03"
    OPTIMIZED_GLOVE_100_BASELINE_CODEMASTER_05 = "optimized glove 100 baseline codemaster 05"
    OPTIMIZED_GLOVE_100_BASELINE_CODEMASTER_07 = "optimized glove 100 baseline codemaster 07"

    OPTIMIZED_GLOVE_200_BASELINE_CODEMASTER_03 = "optimized glove 200 baseline codemaster 03"
    OPTIMIZED_GLOVE_200_BASELINE_CODEMASTER_05 = "optimized glove 200 baseline codemaster 05"
    OPTIMIZED_GLOVE_200_BASELINE_CODEMASTER_07 = "optimized glove 200 baseline codemaster 07"

    OPTIMIZED_GLOVE_300_BASELINE_CODEMASTER_03 = "optimized glove 300 baseline codemaster 03"
    OPTIMIZED_GLOVE_300_BASELINE_CODEMASTER_05 = "optimized glove 300 baseline codemaster 05"
    OPTIMIZED_GLOVE_300_BASELINE_CODEMASTER_07 = "optimized glove 300 baseline codemaster 07"

    W2V_DISTANCE_ASSOCIATOR = "w2v distance associator"
    GLOVE_300_DISTANCE_ASSOCIATOR = "glove 300 distance associator"
    GLOVE_50_DISTANCE_ASSOCIATOR = "glove 50 distance associator"
    GLOVE_100_DISTANCE_ASSOCIATOR = "glove 100 distance associator"
    GLOVE_200_DISTANCE_ASSOCIATOR = "glove 200 distance associator"
    W2V_GLOVE_DISTANCE_ASSOCIATOR = "w2v_glove distance associator"
    CN_NB_DISTANCE_ASSOCIATOR = "cn_nb distance associator"

    W2V_DISTANCE_ASSOCIATOR_GUESSER = "w2v distance associator guesser"
    GLOVE_300_DISTANCE_ASSOCIATOR_GUESSER = "glove 300 distance associator guesser"
    GLOVE_50_DISTANCE_ASSOCIATOR_GUESSER = "glove 50 distance associator guesser"
    GLOVE_100_DISTANCE_ASSOCIATOR_GUESSER = "glove 100 distance associator guesser"
    GLOVE_200_DISTANCE_ASSOCIATOR_GUESSER = "glove 200 distance associator guesser"
    W2V_GLOVE_DISTANCE_ASSOCIATOR_GUESSER = "w2v_glove distance associator guesser"
    CN_NB_DISTANCE_ASSOCIATOR_GUESSER = "cn_nb distance associator guesser"

    DISTANCE_ENSEMBLE_CODEMASTER = "distance ensemble codemaster"
    ASSOCIATOR_ENSEMBLE_CODEMASTER = "associator ensemble codemaster"

    DISTANCE_ENSEMBLE_GUESSER = "distance ensemble guesser"
    ASSOCIATOR_ENSEMBLE_GUESSER = "associator ensemble guesser"

    RANDOM_DISTANCE_ENSEMBLE_GUESSER = "random distance ensemble guesser"
    RANDOM_ASSOCIATOR_ENSEMBLE_GUESSER = "random associator ensemble guesser"
    RANDOM_DISTANCE_ENSEMBLE_CODEMASTER= "random distance ensemble codemaster"
    RANDOM_ASSOCIATOR_ENSEMBLE_CODEMASTER= "random associator ensemble codemaster"


    RANDOM_GUESSER = "random guesser"
    RANDOM_CODEMASTER = "random codemaster"

class AITypes:
    ASSOCIATOR = "associator" 
    DISTANCE_ASSOCIATOR = "distance_associator"
    BASELINE = "baseline" 
    OPTIMIZED_BASELINE = "optimized baseline"
    DISTANCE_ENSEMBLE = "distance ensemble"
    ASSOCIATOR_ENSEMBLE = "associator ensemble"
    RANDOM_DISTANCE_ENSEMBLE = "random distance ensemble"
    RANDOM_ASSOCIATOR_ENSEMBLE = "random associator ensemble"
    RANDOM = "random"

class LMTypes:
    W2V = 0
    W2V_GLOVE_C = 1
    GLOVE_50 = 2
    GLOVE_100 = 3
    GLOVE_200 = 4
    GLOVE_300 = 5
    CN_NB = 6
    W2V_GLOVE_G = 7
    BERT = 8
    CN = 9
    HUMAN = 10
    T5 = 11
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
    ASSOCIATOR_AI_CODEMASTER = 0
    VECTOR_BASELINE_CODEMASTER = 1
    OPTIMIZED_VECTOR_BASELINE_CODEMASTER = 2
    ENSEMBLE_AI_CODEMASTER = 3
    DISTANCE_ASSOCIATOR_AI_CODEMASTER = 4
    RANDOM_CODEMASTER = 5
    ASSOCIATOR_AI_GUESSER = 6
    VECTOR_BASELINE_GUESSER = 7
    ENSEMBLE_AI_GUESSER = 8
    RANDOM_GUESSER = 9
    RANDOM_ENSEMBLE_AI_CODEMASTER = 10
    RANDOM_ENSEMBLE_AI_GUESSER = 11 

