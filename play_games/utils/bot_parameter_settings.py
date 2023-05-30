class BotPaths():
    def __init__(self, bot_types, file_paths_obj):
        self.bot_types = bot_types
        self.file_paths_obj = file_paths_obj
        self.set_paths()
    
    def set_paths(self):
        self.paths = {

            self.bot_types.W2V_GLOVE_BASELINE_GUESSER : [self.file_paths_obj.baseline_w2v_300_source_path, self.file_paths_obj.baseline_glove_300_source_path],
            self.bot_types.W2V_BASELINE_GUESSER : self.file_paths_obj.baseline_w2v_300_source_path,
            self.bot_types.GLOVE_50_BASELINE_GUESSER : self.file_paths_obj.baseline_glove_50_source_path,
            self.bot_types.GLOVE_100_BASELINE_GUESSER : self.file_paths_obj.baseline_glove_100_source_path,
            self.bot_types.GLOVE_200_BASELINE_GUESSER : self.file_paths_obj.baseline_glove_200_source_path,
            self.bot_types.GLOVE_300_BASELINE_GUESSER : self.file_paths_obj.baseline_glove_300_source_path,
            self.bot_types.CN_NB_BASELINE_GUESSER : self.file_paths_obj.baseline_cn_nb_source_path,

            self.bot_types.W2V_GLOVE_DISTANCE_ASSOCIATOR : [self.file_paths_obj.w2v_glove_boardwords_source_path, self.file_paths_obj.baseline_w2v_glove_source_path],
            self.bot_types.W2V_DISTANCE_ASSOCIATOR : [self.file_paths_obj.word2vec_boardwords_source_path, self.file_paths_obj.baseline_w2v_300_source_path],
            self.bot_types.GLOVE_300_DISTANCE_ASSOCIATOR : [self.file_paths_obj.glove_boardwords_source_path, self.file_paths_obj.baseline_glove_300_source_path],
            self.bot_types.GLOVE_50_DISTANCE_ASSOCIATOR : [self.file_paths_obj.glove_50_boardwords_source_path, self.file_paths_obj.baseline_glove_50_source_path],
            self.bot_types.GLOVE_100_DISTANCE_ASSOCIATOR : [self.file_paths_obj.glove_100_boardwords_source_path, self.file_paths_obj.baseline_glove_100_source_path],
            self.bot_types.GLOVE_200_DISTANCE_ASSOCIATOR : [self.file_paths_obj.glove_200_boardwords_source_path, self.file_paths_obj.baseline_glove_200_source_path],
            self.bot_types.CN_NB_DISTANCE_ASSOCIATOR : [self.file_paths_obj.cn_nb_boardwords_source_path, self.file_paths_obj.baseline_cn_nb_source_path],

            self.bot_types.DISTANCE_ENSEMBLE_CODEMASTER: None,
            self.bot_types.DISTANCE_ENSEMBLE_GUESSER: None,

            self.bot_types.RANDOM_DISTANCE_ENSEMBLE_CODEMASTER: None,
            self.bot_types.RANDOM_DISTANCE_ENSEMBLE_GUESSER: None,
        }
    
    def get_paths_for_bot(self, bot_type_key):
        return self.paths[bot_type_key]

class BotAITypes():
    def __init__(self, bot_types, ai_types):
        self.bot_types = bot_types
        self.ai_types = ai_types
        self.set_bot_ai_types()
    
    def set_bot_ai_types(self):
        self.bot_ai_types = { 

            self.bot_types.W2V_GLOVE_BASELINE_GUESSER : self.ai_types.BASELINE,
            self.bot_types.W2V_BASELINE_GUESSER : self.ai_types.BASELINE,
            self.bot_types.GLOVE_50_BASELINE_GUESSER : self.ai_types.BASELINE,
            self.bot_types.GLOVE_100_BASELINE_GUESSER : self.ai_types.BASELINE,
            self.bot_types.GLOVE_200_BASELINE_GUESSER : self.ai_types.BASELINE,
            self.bot_types.GLOVE_300_BASELINE_GUESSER : self.ai_types.BASELINE,
            self.bot_types.CN_NB_BASELINE_GUESSER : self.ai_types.BASELINE,
            
            self.bot_types.W2V_DISTANCE_ASSOCIATOR : self.ai_types.DISTANCE_ASSOCIATOR,
            self.bot_types.GLOVE_300_DISTANCE_ASSOCIATOR : self.ai_types.DISTANCE_ASSOCIATOR,
            self.bot_types.GLOVE_50_DISTANCE_ASSOCIATOR : self.ai_types.DISTANCE_ASSOCIATOR,
            self.bot_types.GLOVE_100_DISTANCE_ASSOCIATOR : self.ai_types.DISTANCE_ASSOCIATOR,
            self.bot_types.GLOVE_200_DISTANCE_ASSOCIATOR : self.ai_types.DISTANCE_ASSOCIATOR,
            self.bot_types.GLOVE_300_DISTANCE_ASSOCIATOR : self.ai_types.DISTANCE_ASSOCIATOR,
            self.bot_types.W2V_GLOVE_DISTANCE_ASSOCIATOR : self.ai_types.DISTANCE_ASSOCIATOR,
            self.bot_types.CN_NB_DISTANCE_ASSOCIATOR : self.ai_types.DISTANCE_ASSOCIATOR,

            self.bot_types.DISTANCE_ENSEMBLE_CODEMASTER : self.ai_types.DISTANCE_ENSEMBLE,
            self.bot_types.DISTANCE_ENSEMBLE_GUESSER : self.ai_types.DISTANCE_ENSEMBLE,

            self.bot_types.RANDOM_DISTANCE_ENSEMBLE_CODEMASTER: self.ai_types.RANDOM_DISTANCE_ENSEMBLE,
            self.bot_types.RANDOM_DISTANCE_ENSEMBLE_GUESSER: self.ai_types.RANDOM_DISTANCE_ENSEMBLE,
        }

    def get_bot_ai_type(self, bot_type_key):
        return self.bot_ai_types[bot_type_key]

class BotLMTypes():
    def __init__(self, bot_types, lm_types):
        self.bot_types = bot_types
        self.lm_types = lm_types
        self.set_bot_lm_types()
    
    def set_bot_lm_types(self):
        self.bot_lm_types = {
            self.bot_types.W2V_GLOVE_DISTANCE_ASSOCIATOR : self.lm_types.W2V_GLOVE_C,
            self.bot_types.W2V_DISTANCE_ASSOCIATOR : self.lm_types.W2V,
            self.bot_types.GLOVE_50_DISTANCE_ASSOCIATOR : self.lm_types.GLOVE_50,
            self.bot_types.GLOVE_100_DISTANCE_ASSOCIATOR : self.lm_types.GLOVE_100,
            self.bot_types.GLOVE_200_DISTANCE_ASSOCIATOR : self.lm_types.GLOVE_200,
            self.bot_types.GLOVE_300_DISTANCE_ASSOCIATOR : self.lm_types.GLOVE_300,
            self.bot_types.CN_NB_DISTANCE_ASSOCIATOR : self.lm_types.CN_NB,

            self.bot_types.W2V_BASELINE_GUESSER : self.lm_types.W2V,
            self.bot_types.GLOVE_50_BASELINE_GUESSER : self.lm_types.GLOVE_50,
            self.bot_types.GLOVE_100_BASELINE_GUESSER : self.lm_types.GLOVE_100,
            self.bot_types.GLOVE_200_BASELINE_GUESSER : self.lm_types.GLOVE_200,
            self.bot_types.GLOVE_300_BASELINE_GUESSER : self.lm_types.GLOVE_300,
            self.bot_types.W2V_GLOVE_BASELINE_GUESSER : self.lm_types.W2V_GLOVE_G, 
            self.bot_types.CN_NB_BASELINE_GUESSER : self.lm_types.CN_NB, 

            self.bot_types.DISTANCE_ENSEMBLE_CODEMASTER : self.lm_types.ENSEMBLE,
            self.bot_types.DISTANCE_ENSEMBLE_GUESSER : self.lm_types.ENSEMBLE,

            self.bot_types.RANDOM_DISTANCE_ENSEMBLE_CODEMASTER: self.lm_types.RANDOM_ENSEMBLE,
            self.bot_types.RANDOM_DISTANCE_ENSEMBLE_GUESSER: self.lm_types.RANDOM_ENSEMBLE,
        }

    def get_bot_lm_type(self, bot_type_key):
        return self.bot_lm_types[bot_type_key]
