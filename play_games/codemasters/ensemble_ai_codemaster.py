import random
import numpy as np
import joblib

#Bot libraries
from ai_components.ensemble_ai_components.ensemble_ai import EnsambleAI
from ai_components.ensemble_ai_components.ensemble_utils import LearningAlgorithms


class EnsembleAICodemaster(EnsambleAI):

    def __init__(self):
        random.seed(42)
        self.learning_algorithms = LearningAlgorithms()

        self.player_words = None
        self.opponent_words = None
        self.bystander_words = None
        self.assassin_word = None

        #We will use bot_clues_generated in order to determine the bots involved and then we'll put them in bots_used
        self.bot_clues_generated = {}
        self.bots_used = {}

        self.total_rounds = 0

        #These help us decide which bots to select. Usage dict helps us to see which ones we haven't tried. 
        #bot weights is what we use to select the bot (Max or min value is chosen)
        self.usage_dict = {}
        self.bot_weights = {}


    def initialize(self, args):
        '''
        We pass in args to mimic having different constructors. If the argument passed in is of the indicated type, we don't want to do anything. 
        '''
        c_name = args.__class__.__name__ 
        if c_name == "BotSettingsObj":
            return

        assert(len(args) == 4)
        bots = args[0]
        bot_types = args[1]
        tm_type = args[2]
        bot_settings = args[3]
        super().__init__(bots, bot_types, bot_settings)

        #Create an instance of the strategy we are using
        self.strategy = self.create_strategy_inner()
        self.strategy.initialize_bot_stats()

        self.log_file = bot_settings.LEARN_LOG_FILE_CM

        if self.log_file is not None:
            str2w = "STARTING TO LEARN\nguesser is: " + tm_type + '\n\n'
            if self.log_file != None: self.log_file.write(str2w)
        

    def create_strategy_inner(self):
        if self.learning_algorithm == self.learning_algorithms.T3:
            return EnsembleAICodemaster.StrategyThree(self)
        elif self.learning_algorithm == self.learning_algorithms.T4:
            return EnsembleAICodemaster.StrategyFour(self)

    def generate_clue(self, player_words, prev_clues, opponent_words, assassin_word, bystander_words):
        self.total_rounds += 1

        self.player_words = player_words
        self.opponent_words = opponent_words
        self.bystander_words = bystander_words
        self.assassin_word = assassin_word


        self.generate_all_bot_clues(player_words, prev_clues, opponent_words, assassin_word, bystander_words)

        #Before we select a bot, we need to update the values from last turn
        self.strategy.update_values()

        bot_to_use = self.strategy.select_bot()
        clue, targets = self.bot_clues_generated[bot_to_use]

        self.determine_contributing_bots(clue)

        self.log_round(bot_to_use)

        return clue, targets

    def give_feedback(self, guess, end_status):

        #if end_status is 0, game hasn't ended. 1 = loss and 2 = win

        self.add_consequences(guess)

        bot_str = ""

        if end_status == 1:
            bot_str += "\nend_status: loss" + '\n'
        elif end_status == 2:
            bot_str += "\nend_status: win" + '\n'

        bot_str += '\n'

        if self.bot_settings.PRINT_LEARNING:
            print(bot_str)
        if self.log_file is not None: self.log_file.write(bot_str)

    ###__________________________HELPER FUNCTIONS________________________###

    def add_consequences(self, guess):
        if guess in self.player_words:
            self.strategy.add_correct_consequence()
        elif guess in self.bystander_words:
            self.strategy.add_bystander_consequence()
        elif guess in self.opponent_words:
            self.strategy.add_opponent_consequence()
        else:
            self.strategy.add_assassin_consequence()


    def generate_all_bot_clues(self, player_words, prev_clues, opponent_words, assassin_word, bystander_words):
        for bot_type, bot in zip(self.bot_types, self.bots):
            clue, targets = bot.generate_clue(player_words, prev_clues, opponent_words, assassin_word, bystander_words)
            self.bot_clues_generated[bot_type] = (clue, targets)

    def determine_contributing_bots(self, clue):
        #see what bots generated the clue
        self.bots_used.clear()
        for key in self.bot_clues_generated.keys():
            curr_clue, curr_targets = self.bot_clues_generated[key]
            if curr_clue == clue:
                #Update bot streaks
                self.bots_used[key] = 1
                self.usage_dict[key] += 1
    

    ###__________________________LOGGER FUNCTIONS________________________###

    def get_bot_clues_generated(self):
        bot_str = ''
        for key in self.bot_clues_generated.keys():
            bot = key
            clue = self.bot_clues_generated[key][0]
            bot_str += bot + ": " + clue + '\n'

        return bot_str
    
    def get_bot_weights(self):
        bot_str = ''
        for key in self.bot_weights.keys():
            bot = key
            weight = self.bot_weights[key]
            bot_str += bot + ": " + str(weight) + "\n"
        return bot_str

    def log_round(self, bot_to_use):
        if self.log_file is not None:
            str2w = f"BOT SELECTION STAGE\nbot clues:\n{self.get_bot_clues_generated()}\nUCB Constant: {self.ucb_constant}\nbot weights:\n{self.get_bot_weights()}\nchosen bot: {bot_to_use}\n\n" \
                    + f"FEEDBACK STAGE\n"
            if self.bot_settings.PRINT_LEARNING:
                print(str2w)
            
            if self.log_file != None: self.log_file.write(str2w)
    

 ###__________________________STRATEGY CLASSES________________________###

    #This strategy uses 36 features representing the probability of an individual turn outcome 
    class StrategyThree(object):

        def __init__(self, ensamble_cm_instance):
            self.outer = ensamble_cm_instance
            self.model = joblib.load(self.outer.bot_settings.MODEL_PATH)
            self.bot_stats = {}
            self.pos_events = []
            self.event_dict = {}

            self.red_flipped = 0
            self.blue_flipped = 0
            self.bystander_flipped = 0
            self.assassin_flipped = 0

        def select_bot(self):
            return max(self.outer.bot_weights, key=self.outer.bot_weights.get)

        def initialize_bot_stats(self):
            self.generate_pos_events()
            for bot in self.outer.bot_types:
                #I need to initalize a dictionary containing all of the possible turns and their counts for each bot
                self.outer.usage_dict[bot] = 0
                self.outer.bot_weights[bot] = np.inf
                self.bot_stats[bot] = self.event_dict.copy()

        def update_values(self):
            # I need to add the previous turn outcome to bot_stats
            self.add_prev_turn_result()
            for key in self.outer.bot_weights:
                total_rounds_used = self.outer.usage_dict[key] + 1

                curr_score = self.calculate_score(key) 
                
                self.outer.bot_weights[key] = curr_score + (self.outer.ucb_constant * (np.sqrt(np.log(self.outer.total_rounds) / total_rounds_used)))
            
            #We set the words flipped back to zero for next turn
            self.red_flipped = 0
            self.blue_flipped = 0
            self.bystander_flipped = 0
            self.assassin_flipped = 0

        def add_correct_consequence(self):
            self.red_flipped += 1
                
        def add_bystander_consequence(self):
            self.bystander_flipped += 1

        def add_opponent_consequence(self):
            self.blue_flipped += 1

        def add_assassin_consequence(self):
            self.assassin_flipped += 1

        ###---Strategy Helper Functions---###
        def add_prev_turn_result(self):
            #I need to create the correct key
            key = str(self.red_flipped) + str(self.blue_flipped) + str(self.bystander_flipped) + str(self.assassin_flipped)
            #If we're on the first round, bots_used will be empty so we don't need to worry about indexing into a non-existent key. 
            for bot in self.outer.bots_used:
                self.bot_stats[bot][key] += 1

        def get_x(self, key):
            total_events = sum(self.bot_stats[key].values())
            x = []
            for event in self.pos_events:
                if total_events != 0:
                    x.append(self.bot_stats[key][event] / total_events)
                else:
                    x.append(0)
            return x

        def calculate_score(self, key):
            #check to see if it's been used yet, if it hasn't, then it's score is infinity
            if self.outer.usage_dict[key] == 0:
                return np.inf
                
            x = self.get_x(key)
            y = self.model.predict([x])[0]
            return y

        def generate_pos_events(self):
            self.event_dict = {}
            for r in range(10):
                c = 0
                for b in [None, 'theirs', 'by', 'assassin']:
                    
                    if r == 0 and (b is None):
                        c += 1
                        continue
                    if r == 9 and (b is not None):
                        c += 1
                        continue

                    key = [r, 0, 0, 0]
                    if c > 0:
                        key[c] = 1
                    c += 1
                    key_str = self.create_string(key)
                    self.pos_events.append(key_str)
                    self.event_dict[key_str] = 0

        def create_string(self, arr):
            res = ''
            for num in arr:
                res += str(num)
            return res

    #This strategy randomly selects an arm
    class StrategyFour(object):

        def __init__(self, ensamble_cm_instance):
            self.outer = ensamble_cm_instance

        def select_bot(self):
            return random.choice(self.outer.bot_types)

        def initialize_bot_stats(self):
            for bot in self.outer.bot_types:
                #I need to initalize a dictionary containing all of the possible turns and their counts for each bot
                self.outer.usage_dict[bot] = 0
                self.outer.bot_weights[bot] = 0


        def update_values(self):
            pass

        def add_correct_consequence(self):
            pass
                
        def add_bystander_consequence(self):
            pass

        def add_opponent_consequence(self):
            pass

        def add_assassin_consequence(self):
            pass