import ai_components.ensemble_ai_components.ensemble_utils as EnsambleUtils
import scipy.spatial.distance as distance



class EnsambleAI:
    def __init__(self, bots, bot_types, bot_settings):
        self.parameters = bot_settings.ENSEMBLE_PARAMS
        self.bots = bots
        self.bot_types = bot_types
        self.bot_settings = bot_settings
        self.ucb_constant = self.bot_settings.ENSEMBLE_PARAMS
        if self.bot_settings.LEARNING_ALGORITHM in EnsambleUtils.LearningAlgorithms.IMPLEMENTED_ALGORITHMS:
            self.learning_algorithm = self.bot_settings.LEARNING_ALGORITHM
        else:
            print("No learning algorithm")

    def load_dict(self, boardwords):
        for bot in self.bots:
            bot.load_dict(boardwords)
    
    def initialize_bots(self):
        pass

    def give_feedback(self, val):
        pass
    
    def get_cos_dist(self, arr_1, arr_2):
        return distance.cosine(arr_1, arr_2)