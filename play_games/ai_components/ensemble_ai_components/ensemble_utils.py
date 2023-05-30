class LearningAlgorithms:
    T3 = "T3"
    T4 = "T4"
    IMPLEMENTED_ALGORITHMS = [T3, T4]
    
class EnsembleCodemasterBots():
    def __init__(self, ai_types, bot_types):
        self.ai_types = ai_types
        self.bot_types = bot_types
        self.set_ensemble_cm_bots()
    
    def set_ensemble_cm_bots(self):
        self.ensemble_cm_bots = {
            self.ai_types.DISTANCE_ENSEMBLE: [self.bot_types.W2V_DISTANCE_ASSOCIATOR, self.bot_types.GLOVE_50_DISTANCE_ASSOCIATOR, self.bot_types.GLOVE_100_DISTANCE_ASSOCIATOR, \
                self.bot_types.GLOVE_200_DISTANCE_ASSOCIATOR, self.bot_types.GLOVE_300_DISTANCE_ASSOCIATOR, self.bot_types.W2V_GLOVE_DISTANCE_ASSOCIATOR, self.bot_types.CN_NB_DISTANCE_ASSOCIATOR],
            self.ai_types.RANDOM_DISTANCE_ENSEMBLE: [self.bot_types.W2V_DISTANCE_ASSOCIATOR, self.bot_types.GLOVE_50_DISTANCE_ASSOCIATOR, self.bot_types.GLOVE_100_DISTANCE_ASSOCIATOR, \
                self.bot_types.GLOVE_200_DISTANCE_ASSOCIATOR, self.bot_types.GLOVE_300_DISTANCE_ASSOCIATOR, self.bot_types.W2V_GLOVE_DISTANCE_ASSOCIATOR, self.bot_types.CN_NB_DISTANCE_ASSOCIATOR]
        }
    
    def get_ensemble_cm_bots(self, ai_type_key):
        return self.ensemble_cm_bots[ai_type_key]

class EnsembleGuesserBots():
    def __init__(self, ai_types, bot_types):
        self.ai_types = ai_types
        self.bot_types = bot_types
        self.set_ensemble_g_bots()
    
    def set_ensemble_g_bots(self):
        self.ensemble_g_bots = {
            self.ai_types.DISTANCE_ENSEMBLE: [self.bot_types.W2V_BASELINE_GUESSER, self.bot_types.GLOVE_50_BASELINE_GUESSER, self.bot_types.GLOVE_100_BASELINE_GUESSER, \
                self.bot_types.GLOVE_200_BASELINE_GUESSER, self.bot_types.GLOVE_300_BASELINE_GUESSER, self.bot_types.W2V_GLOVE_BASELINE_GUESSER, self.bot_types.CN_NB_BASELINE_GUESSER],
            self.ai_types.RANDOM_DISTANCE_ENSEMBLE: [self.bot_types.W2V_BASELINE_GUESSER, self.bot_types.GLOVE_50_BASELINE_GUESSER, self.bot_types.GLOVE_100_BASELINE_GUESSER, \
                self.bot_types.GLOVE_200_BASELINE_GUESSER, self.bot_types.GLOVE_300_BASELINE_GUESSER, self.bot_types.W2V_GLOVE_BASELINE_GUESSER, self.bot_types.CN_NB_BASELINE_GUESSER]
        }
    
    def get_ensemble_g_bots(self, ai_type_key):
        return self.ensemble_g_bots[ai_type_key]
