import copy

#object imports
from utils.experiment_settings import ExperimentSettings
from utils.file_manager import FileManager
from utils.file_name_directory_elements import FileNameDirectoryElements
from utils.file_paths_obj import FilePathsObj
from utils.results_analyzer import ResultsAnalyzer
from utils.utils import Parameters, BotTypes, AITypes, LMTypes, ConfigKeys, ExperimentTypes, BotConstructorTypes
from utils.bot_settings_obj import BotSettingsObj
from utils.bot_parameter_settings import BotAITypes, BotLMTypes, BotPaths
from utils.analysis_files.parsers.round_log_parser import RoundLogParser
from utils.analysis_files.parsers.learn_log_parser import LearnLogParser
from utils.analysis_files.analysis_utils import RoundParseKeys, LearnParseKeys, StatDictKeys, Stats, MinMaxKeys, DesiredStats, DesiredStatsKeys
from utils.bot_initializer import BotInitializer
from utils.bot_objects import BotObjects
from ai_components.ensemble_ai_components.ensemble_utils import EnsembleCodemasterBots, EnsembleGuesserBots

#bot imports
from codemasters.associator_ai_codemaster import AssociatorAICodemaster
from codemasters.vector_baseline_codemaster import VectorBaselineCodemaster
from codemasters.optimized_vector_baseline_codemaster import OptimizedVectorBaselineCodemaster
from codemasters.ensemble_ai_codemaster import EnsembleAICodemaster
from codemasters.distance_associator_ai_codemaster import DistanceAssociatorAICodemaster
from codemasters.random_codemaster import RandomCodemaster

from guessers.associator_ai_guesser import AssociatorAIGuesser
from guessers.vector_baseline_guesser import VectorBaselineGuesser
from guessers.ensemble_ai_guesser import EnsembleAIGuesser
from guessers.random_guesser import RandomGuesser

#function imports
from utils.utils import cond_print

#array imports
from utils.analysis_files.analysis_utils import MAIN_STATS_KEYS, PERFORMANCE_PROGRESSION_STATS, PERFORMANCE_PROGRESSION_SLIDING_WINDOW_STATS

class ObjectManager:
    def __init__(self):
        #independent imported arrays
        self.main_stat_keys = MAIN_STATS_KEYS
        self.performance_progression_stat_keys = PERFORMANCE_PROGRESSION_STATS
        self.performance_progression_sliding_window_stat_keys = PERFORMANCE_PROGRESSION_SLIDING_WINDOW_STATS
        
        #independent object instantiation
        self.lm_types = LMTypes()
        self.bot_types = BotTypes()
        self.ai_types = AITypes()
        self.parameters = Parameters()
        self.config_keys = ConfigKeys()
        self.experiment_types = ExperimentTypes()
        self.bot_constructor_types = BotConstructorTypes()
        self.stats = Stats()
        self.learn_parse_keys = LearnParseKeys()
        self.round_parse_keys = RoundParseKeys()
        self.min_max_keys = MinMaxKeys()
        self.desired_stats_keys = DesiredStatsKeys()
        self.file_name_directory_elements = FileNameDirectoryElements()
        self.file_paths_obj = FilePathsObj()
        self.stat_dict_keys = StatDictKeys()
        self.bot_settings_obj = BotSettingsObj()
        #dependent object instantiation
        self.desired_stats = DesiredStats(self.stats, self.desired_stats_keys, self.min_max_keys)
        self.bot_paths = BotPaths(self.bot_types, self.file_paths_obj)
        self.bot_ai_types = BotAITypes(self.bot_types, self.ai_types)
        self.bot_lm_types = BotLMTypes(self.bot_types, self.lm_types)
        self.experiment_settings = ExperimentSettings(self.experiment_types, self.file_paths_obj, self.config_keys)
        self.round_log_parser = RoundLogParser(self.round_parse_keys, self.stats)
        self.learn_log_parser = LearnLogParser(self.learn_parse_keys, self.stats) 
        self.ensemble_cm_bots = EnsembleCodemasterBots(self.ai_types, self.bot_types)
        self.ensemble_g_bots = EnsembleGuesserBots(self.ai_types, self.bot_types)
        #double-dependent objects (depend on dependent objects and independent objects)
        self.file_manager = FileManager(self.experiment_settings, self.ai_types, self.file_paths_obj, self.bot_ai_types, self.experiment_types, self.file_name_directory_elements, self.parameters, self.performance_progression_stat_keys, self.performance_progression_sliding_window_stat_keys, self.main_stat_keys)
        self.results_analyzer = ResultsAnalyzer(self.experiment_settings, self.file_paths_obj, self.round_log_parser, self.learn_log_parser, \
            self.stats, self.stat_dict_keys, self.experiment_types, self.bot_ai_types, self.ai_types, self.main_stat_keys, self.performance_progression_stat_keys, \
            self.performance_progression_sliding_window_stat_keys, self.desired_stats, \
            self.desired_stats_keys, self.min_max_keys, self.lm_types, self.bot_lm_types)
        self.bot_objects_arg = self.create_bot_objects_arg()
        self.bot_objects = BotObjects(self.bot_objects_arg)
        self.bot_initializer = BotInitializer(self.bot_types, self.ai_types, self.bot_ai_types, self.bot_lm_types, self.bot_paths, self.bot_objects, self.bot_constructor_types, \
            self.ensemble_cm_bots, self.ensemble_g_bots)
        #independent imported functions
        self.cond_print = cond_print
    

    '''
    We put this in the object manager because we want all local imports to occur in the object manager. Because the bot imports are local, we create a dictionary of the constructors and pass it into the BotObjects object so 
    that we can create new bot objects throughout the code. 
    '''
    def create_bot_objects_arg(self):
        bot_objects_arg = {
            BotConstructorTypes.ASSOCIATOR_AI_CODEMASTER : AssociatorAICodemaster(),
            BotConstructorTypes.VECTOR_BASELINE_CODEMASTER : VectorBaselineCodemaster(),
            BotConstructorTypes.OPTIMIZED_VECTOR_BASELINE_CODEMASTER : OptimizedVectorBaselineCodemaster(),
            BotConstructorTypes.ENSEMBLE_AI_CODEMASTER : EnsembleAICodemaster(),
            BotConstructorTypes.DISTANCE_ASSOCIATOR_AI_CODEMASTER : DistanceAssociatorAICodemaster(),
            BotConstructorTypes.RANDOM_CODEMASTER : RandomCodemaster(),
            BotConstructorTypes.ASSOCIATOR_AI_GUESSER : AssociatorAIGuesser(), 
            BotConstructorTypes.VECTOR_BASELINE_GUESSER : VectorBaselineGuesser(),
            BotConstructorTypes.ENSEMBLE_AI_GUESSER : EnsembleAIGuesser(),
            BotConstructorTypes.RANDOM_GUESSER : RandomGuesser(),
        }
        return bot_objects_arg
    
    def get_new_bot_settings_obj(self):
        return copy.deepcopy(self.bot_settings_obj)
    
        


    
    