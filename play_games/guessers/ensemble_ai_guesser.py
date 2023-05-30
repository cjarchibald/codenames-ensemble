import random
import numpy as np
import joblib

#Bot libraries
from ai_components.ensemble_ai_components.ensemble_ai import EnsambleAI
from ai_components.ensemble_ai_components.ensemble_utils import LearningAlgorithms


class EnsembleAIGuesser(EnsambleAI):

    def __init__(self):
        random.seed(42)
        self.learning_algorithms = LearningAlgorithms()

        #After guess is decided on, these will be set so we can refer to them in the feedback stage
        self.curr_guesses = None

        #We will use bot_guesses_generated in order to determine the bots involved and then we'll put them in bots_used
        self.bot_guesses_generated = {}
        self.bots_used = {}

        #These help us decide which bots to select. Usage dict helps us to see which ones we haven't tried. 
        #bot weights is what we use to select the bot (Max or min value is chosen)
        self.usage_dict = {}
        self.bot_weights = {}

        self.total_rounds = 0


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

        self.log_file = bot_settings.LEARN_LOG_FILE_G

        if self.log_file is not None:
            str2w = "STARTING TO LEARN\ncodemaster is: " + tm_type + '\n\n'
            if self.log_file != None: self.log_file.write(str2w)
        

    def create_strategy_inner(self):
        if self.learning_algorithm == self.learning_algorithms.T1:
            return EnsembleAIGuesser.StrategyOne(self)
        elif self.learning_algorithm == self.learning_algorithms.T2:
            return EnsembleAIGuesser.StrategyTwo(self)
        elif self.learning_algorithm == self.learning_algorithms.T3:
            return EnsembleAIGuesser.StrategyThree(self)
        elif self.learning_algorithm == self.learning_algorithms.T4:
            return EnsembleAIGuesser.StrategyFour(self)

    def guess_clue(self, clue, num_guesses, prev_guesses):
        self.total_rounds += 1

        self.generate_all_bot_guesses(clue, num_guesses, prev_guesses)

        #Before we select a bot, we need to update the values from last turn
        self.strategy.update_values()

        bot_to_use = self.strategy.select_bot()
        guesses = self.bot_guesses_generated[bot_to_use]

        self.determine_contributing_bots(guesses)

        self.log_round(bot_to_use)

        self.curr_guesses = guesses

        return guesses

    def give_feedback(self, end_status, word_type):

        #if end_status is 0, game hasn't ended. 1 = loss and 2 = win

        self.add_consequences(word_type)

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

    def add_consequences(self, word_type):
        if word_type == 0:
            self.strategy.add_correct_consequence()
        elif word_type == 2:
            self.strategy.add_bystander_consequence()
        elif word_type == 1:
            self.strategy.add_opponent_consequence()
        else:
            self.strategy.add_assassin_consequence()
    
    def generate_all_bot_guesses(self, clue, num_guesses, prev_guesses):
        for bot_type, bot in zip(self.bot_types, self.bots):
            guesses = bot.guess_clue(clue, num_guesses, prev_guesses)
            self.bot_guesses_generated[bot_type] = guesses
        
        bot_str = ''
        for key in self.bot_guesses_generated.keys():
            bot = key
            guesses = self.bot_guesses_generated[key]
            bot_str += bot + ": " + str(guesses) + '\n'

        return bot_str

    def determine_contributing_bots(self, guesses):
        #see what bots generated the clue
        self.bots_used.clear()
        for key in self.bot_guesses_generated.keys():
            curr_guesses = self.bot_guesses_generated[key]
            #We add the percentage of guesses that a bot had the same
            same_guesses = [g for g in guesses if g in curr_guesses]
            percent_contribution = len(same_guesses) / len(guesses)
            if percent_contribution > 0:
                self.bots_used[key] = percent_contribution
                self.usage_dict[key] += percent_contribution

    ###__________________________LOGGER FUNCTIONS________________________###

    def get_bot_guesses_generated(self):
        bot_str = ''
        for key in self.bot_guesses_generated.keys():
            bot = key
            guesses = self.bot_guesses_generated[key]
            bot_str += bot + ": " + " ,".join(guesses) + '\n'

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
            str2w = f"BOT SELECTION STAGE\nbot guesses:\n{self.get_bot_guesses_generated()}\nUCB Constant: {self.ucb_constant}\nbot weights:\n{self.get_bot_weights()}\nchosen bot: {bot_to_use}\n\n" \
                    + "FEEDBACK STAGE\n"
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
                self.bot_stats[bot][key] += self.outer.bots_used[bot]

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