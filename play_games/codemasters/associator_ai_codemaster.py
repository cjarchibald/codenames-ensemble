'''
This will contain an AssociatorAI and will use its boardlist properties to generate clues

authors: Kyle Rogers and Spencer Brosnahan
'''
from ai_components.associator_ai_components.associator import Associator
from ai_components.ai_components_utils import arr_not_in_word
import random


class AssociatorAICodemaster(Associator):
    def __init__(self):
        self.max_clue_num = 10
        self.opp_clue_freq_limit = 0
        self.bystander_clue_freq_limit = 0
        random.seed(42)

    def initialize(self, settings_obj):
        super().__init__(settings_obj.N_ASSOCIATIONS, settings_obj.CONSTRUCTOR_PATHS, settings_obj.LOG_FILE)

    def generate_clue(self, player_words, prev_clues, opponent_words, assassin_word, bystander_words):
        # find max occurrence - this will be the clue (see fixme comment above)
        clue, ties = self.find_best_clue(player_words, prev_clues, opponent_words, assassin_word, bystander_words)
        random_clues = 0

        # find matching target words
        target_words = []
        for key in self.board_dict:
            if clue in self.board_dict[key] and key in player_words:
                target_words.append(key)
        
        if len(target_words) == 0:
            target_words.append("")
            random_clues = 1

        if self.log_file:  
            self.log_file.write(f"random_clues: {random_clues}\n")

        return clue, target_words
    
    def find_best_clue(self, player_words, prev_clues, opponent_words, assassin_word, bystander_words):
        player_dict = {}
        opp_dict = {}
        bystander_dict = {}

        # build the player dict, opponent dict
        for key in self.board_dict:
            if key in player_words:
                wset = self.board_dict[key]
                for w in wset:
                    if w in player_dict:
                        player_dict[w] += 1
                    else:
                        player_dict[w] = 1
            elif key in opponent_words:
                wset = self.board_dict[key]
                for w in wset:
                    if w in opp_dict:
                        opp_dict[w] += 1
                    else:
                        opp_dict[w] = 1
            else:
                wset = self.board_dict[key]
                for w in wset:
                    if w in bystander_dict:
                        bystander_dict[w] += 1
                    else:
                        bystander_dict[w] = 1

        if len(player_dict) == 0:
            return self.generate_random_clue(prev_clues), 0

        clue_num = max(player_dict.values())
        clue = max(player_dict, key=player_dict.get)

        ct = 0
        while clue_num > self.max_clue_num or clue in prev_clues \
                or (clue in opp_dict and opp_dict[clue] > self.opp_clue_freq_limit) \
                or (clue in bystander_dict and bystander_dict[clue] > self.bystander_clue_freq_limit) \
                or clue in self.board_dict[assassin_word] \
                or clue in self.board_dict.keys() \
                or not arr_not_in_word(clue, player_words + opponent_words + [assassin_word] + bystander_words):
            # to limit the inf loop here
            if ct > 100:
                clue = ''
                break
            player_dict[clue] = -1
            clue_num = max(player_dict.values())
            clue = max(player_dict, key=player_dict.get)

            ct += 1

        # calculate ties in freq
        tie_ct = 0
        ties = {}


        if tie_ct > 1:
            # find ranking between ties
            min_val = float('inf')
            clue = ''
            tie_ct = 0
            # finding optimal clue
            for tie in ties:
                val = ties[tie]
                if val < min_val:
                    clue = tie
                    min_val = val

        return clue, tie_ct
    
    def generate_random_clue(self, prev_clues):
        wordpool = [w for w in self.datacache.wordlist if w not in prev_clues]
        return random.choice(wordpool)