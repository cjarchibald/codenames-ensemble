import copy

class BotInitializer():
    def __init__(self, bot_types, ai_types, bot_ai_types, bot_lm_types, bot_paths, bot_objects, bot_constructor_types, ensemble_cm_types, ensemble_g_types):
        self.bot_types = bot_types
        self.ai_types = ai_types
        self.bot_ai_types = bot_ai_types
        self.bot_lm_types = bot_lm_types
        self.bot_paths = bot_paths
        self.bot_objects = bot_objects
        self.bot_constructor_types = bot_constructor_types
        self.ensemble_cm_types = ensemble_cm_types
        self.ensemble_g_types = ensemble_g_types
        self.orig_alg = None
    

    '''
    We use the ai_type to determine the constructor we need because each constructor is built for a specific ai_type and the filepaths determine which lm is used. 
    If we simply used the bot_type to determine which constructor to call, we would have a lot more conditional blocks and/or conditions. 
    '''
    def init_bots(self, bot_type_1, bot_type_2, bot_settings):
        codemaster_bot = None
        guesser_bot = None
        if self.orig_alg == None: self.orig_alg = bot_settings.LEARNING_ALGORITHM #assign this if it is the first time it is called

        if bot_type_1 != None:
            bot_settings.CONSTRUCTOR_PATHS = self.bot_paths.get_paths_for_bot(bot_type_1)
            if self.bot_ai_types.get_bot_ai_type(bot_type_1) == self.ai_types.ASSOCIATOR:
                codemaster_bot = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.ASSOCIATOR_AI_CODEMASTER)
            elif self.bot_ai_types.get_bot_ai_type(bot_type_1) == self.ai_types.DISTANCE_ASSOCIATOR:
                codemaster_bot = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.DISTANCE_ASSOCIATOR_AI_CODEMASTER)
            elif self.bot_ai_types.get_bot_ai_type(bot_type_1) == self.ai_types.BASELINE:
                codemaster_bot = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.VECTOR_BASELINE_CODEMASTER)
            elif self.bot_ai_types.get_bot_ai_type(bot_type_1) == self.ai_types.OPTIMIZED_BASELINE:
                codemaster_bot = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.OPTIMIZED_VECTOR_BASELINE_CODEMASTER)
            elif self.bot_ai_types.get_bot_ai_type(bot_type_1) == self.ai_types.DISTANCE_ENSEMBLE:
                codemaster_bot = self.initialize_ensemble_cm(self.ai_types.DISTANCE_ENSEMBLE, bot_type_2, bot_settings)
            elif self.bot_ai_types.get_bot_ai_type(bot_type_1) == self.ai_types.RANDOM_DISTANCE_ENSEMBLE:
                codemaster_bot = self.initialize_ensemble_cm(self.ai_types.RANDOM_DISTANCE_ENSEMBLE, bot_type_2, bot_settings)
            elif self.bot_ai_types.get_bot_ai_type(bot_type_1) == self.ai_types.ASSOCIATOR_ENSEMBLE:
                codemaster_bot = self.initialize_ensemble_cm(self.ai_types.ASSOCIATOR_ENSEMBLE, bot_type_2, bot_settings)
            elif self.bot_ai_types.get_bot_ai_type(bot_type_1) == self.ai_types.RANDOM_ASSOCIATOR_ENSEMBLE:
                codemaster_bot = self.initialize_ensemble_cm(self.ai_types.RANDOM_ASSOCIATOR_ENSEMBLE, bot_type_2, bot_settings)
            elif self.bot_ai_types.get_bot_ai_type(bot_type_1) == self.ai_types.RANDOM:
                codemaster_bot = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.RANDOM_CODEMASTER)
            else:
                print("Error loading codemaster")
                return

            codemaster_bot.initialize(bot_settings)
        
        if bot_type_2 != None:
            bot_settings.CONSTRUCTOR_PATHS = self.bot_paths.get_paths_for_bot(bot_type_2)
            if self.bot_ai_types.get_bot_ai_type(bot_type_2) == self.ai_types.ASSOCIATOR:
                guesser_bot = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.ASSOCIATOR_AI_GUESSER)
            elif self.bot_ai_types.get_bot_ai_type(bot_type_2) == self.ai_types.BASELINE:
                guesser_bot = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.VECTOR_BASELINE_GUESSER)
            elif self.bot_ai_types.get_bot_ai_type(bot_type_2) == self.ai_types.DISTANCE_ENSEMBLE:
                guesser_bot = self.initialize_ensemble_g(self.ai_types.DISTANCE_ENSEMBLE, bot_type_1, bot_settings)
            elif self.bot_ai_types.get_bot_ai_type(bot_type_2) == self.ai_types.ASSOCIATOR_ENSEMBLE:
                guesser_bot = self.initialize_ensemble_g(self.ai_types.ASSOCIATOR_ENSEMBLE, bot_type_1, bot_settings)
            elif self.bot_ai_types.get_bot_ai_type(bot_type_2) == self.ai_types.RANDOM_DISTANCE_ENSEMBLE:
                guesser_bot = self.initialize_ensemble_g(self.ai_types.RANDOM_DISTANCE_ENSEMBLE, bot_type_1, bot_settings)
            elif self.bot_ai_types.get_bot_ai_type(bot_type_2) == self.ai_types.RANDOM_ASSOCIATOR_ENSEMBLE:
                guesser_bot = self.initialize_ensemble_g(self.ai_types.RANDOM_ASSOCIATOR_ENSEMBLE, bot_type_1, bot_settings)
            elif self.bot_ai_types.get_bot_ai_type(bot_type_2) == self.ai_types.RANDOM:
                guesser_bot = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.RANDOM_GUESSER)
            else:
                print("Error loading guesser")
                return 

            guesser_bot.initialize(bot_settings)
        return codemaster_bot, guesser_bot

    '''
    Ensemble bots are special because they depend on other bots. To avoid a lot of code duplication and unnecessary dependencies within
    the bot itself, we will manage the selection of bots to be used and their initialization here.  
    '''
    def initialize_ensemble_cm(self, ai_type, guesser_type, bot_settings):
        if ai_type == self.ai_types.DISTANCE_ENSEMBLE:
            bot_settings.AI_TYPE = self.ai_types.DISTANCE_ENSEMBLE
            bot_settings.LEARNING_ALGORITHM = self.orig_alg
            constructor = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.ENSEMBLE_AI_CODEMASTER)
        elif ai_type == self.ai_types.ASSOCIATOR_ENSEMBLE:
            bot_settings.AI_TYPE = self.ai_types.ASSOCIATOR_ENSEMBLE
            bot_settings.LEARNING_ALGORITHM = self.orig_alg
            constructor = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.ENSEMBLE_AI_CODEMASTER)
        elif ai_type == self.ai_types.RANDOM_ASSOCIATOR_ENSEMBLE:
            bot_settings.AI_TYPE = self.ai_types.RANDOM_ASSOCIATOR_ENSEMBLE
            bot_settings.LEARNING_ALGORITHM = "T4"
            constructor = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.ENSEMBLE_AI_CODEMASTER)
        elif ai_type == self.ai_types.RANDOM_DISTANCE_ENSEMBLE:
            bot_settings.AI_TYPE = self.ai_types.RANDOM_DISTANCE_ENSEMBLE
            bot_settings.LEARNING_ALGORITHM = "T4"
            #Set the file to write to to none 
            bot_settings.LEARN_LOG_FILE_CM = None 
            constructor = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.ENSEMBLE_AI_CODEMASTER)
        else:
            print("Error loading ensemble codemaster")
            return

        # Now that we have the ensemble object, we need to get all of the desired bots and then pass them into the initialization function 
        # We need to know if we want the same lm or not. 

        underlying_bot_types = self.ensemble_cm_types.get_ensemble_cm_bots(ai_type)
        bots = []
        bot_types = []
        for b_type in underlying_bot_types:
            #Because I know that I won't be calling an ensemble bot, I can call init bots with each underlying bot
            assert(bot_settings.INCLUDE_SAME_LM != None)
            if not bot_settings.INCLUDE_SAME_LM and self.bot_lm_types.get_bot_lm_type(b_type) == self.bot_lm_types.get_bot_lm_type(guesser_type):
                continue 
            curr_bot, _ = self.init_bots(b_type, None, bot_settings)
            bots.append(curr_bot)
            bot_types.append(b_type)

        args = (bots, bot_types, guesser_type, bot_settings)
        constructor.initialize(args)
        return constructor
    
    def initialize_ensemble_g(self, ai_type, codemaster_type, bot_settings):
        if ai_type == self.ai_types.DISTANCE_ENSEMBLE:
            bot_settings.AI_TYPE = self.ai_types.DISTANCE_ENSEMBLE
            bot_settings.LEARNING_ALGORITHM = self.orig_alg
            constructor = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.ENSEMBLE_AI_GUESSER)
        elif ai_type == self.ai_types.ASSOCIATOR_ENSEMBLE:
            bot_settings.AI_TYPE = self.ai_types.ASSOCIATOR_ENSEMBLE
            bot_settings.LEARNING_ALGORITHM = self.orig_alg
            constructor = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.ENSEMBLE_AI_GUESSER)
        elif ai_type == self.ai_types.RANDOM_ASSOCIATOR_ENSEMBLE:
            bot_settings.AI_TYPE = self.ai_types.RANDOM_ASSOCIATOR_ENSEMBLE
            bot_settings.LEARNING_ALGORITHM = "T4"
            constructor = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.ENSEMBLE_AI_GUESSER)
        elif ai_type == self.ai_types.RANDOM_DISTANCE_ENSEMBLE:
            bot_settings.AI_TYPE = self.ai_types.RANDOM_DISTANCE_ENSEMBLE
            bot_settings.LEARNING_ALGORITHM = "T4"
            bot_settings.LEARN_LOG_FILE_G = None 
            constructor = self.bot_objects.get_bot_object_copy(self.bot_constructor_types.ENSEMBLE_AI_GUESSER)
        else:
            print("Error loading ensemble guesser")
            return

        # Now that we have the ensemble object, we need to get all of the desired bots and then pass them into the initialization function 
        # We need to know if we want the same lm or not. 

        underlying_bot_types = self.ensemble_g_types.get_ensemble_g_bots(ai_type)
        bots = []
        bot_types = []
        for b_type in underlying_bot_types:
            #Because I know that I won't be calling an ensemble bot, I can call init bots with each underlying bot
            assert(bot_settings.INCLUDE_SAME_LM != None)
            if not bot_settings.INCLUDE_SAME_LM and self.bot_lm_types.get_bot_lm_type(b_type) == self.bot_lm_types.get_bot_lm_type(codemaster_type):
                continue 
            _, curr_bot = self.init_bots(None, b_type, bot_settings)
            bots.append(curr_bot)
            bot_types.append(b_type)

        #change the learning algorthim if needed 
        args = (bots, bot_types, codemaster_type, bot_settings)
        constructor.initialize(args)
        return constructor
        