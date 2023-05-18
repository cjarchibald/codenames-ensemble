'''
This will contain an associatorAI and will use it to generate guesses

authors: Kyle Rogers and Spencer Brosnahan
'''
from ai_components.associator_ai_components.associator import Associator
import random
import copy


def lemmatize(clue, association):
    if clue == association:
        return True
    return False

class AssociatorAIGuesser(Associator):
    def __init__(self):
        pass
    
    def initialize(self, settings_obj):
        super().__init__(settings_obj.N_ASSOCIATIONS, settings_obj.CONSTRUCTOR_PATHS, settings_obj.LOG_FILE)
    
    def guess_clue(self, clue, num_guess, prev_guesses):
        # examine board dict and guess words that have
        guesses = []  # will be len=num_guess
        for gw in self.board_dict:
            for association in self.board_dict[gw]:
                if lemmatize(clue, association) and gw not in prev_guesses:
                    guesses.append(gw)
                    break  # break inner loop since we already found a guess word

        if len(guesses) < num_guess:
            # examine extended dict
            #self.load_ext_dict
            for gw in self.ext_board_dict:
                for association in self.ext_board_dict[gw]:
                    if lemmatize(clue, association) and association not in prev_guesses:
                        guesses.append(gw)
                        break

        return self.default_clue_selection(guesses, num_guess, prev_guesses)

    def default_clue_selection(self, guesses, num_guess, prev_guesses):
        # turn off random guessing
        rand_guesses = 0
        if len(guesses) > 1:
            if self.log_file is not None:
                self.log_file.write(f"random_guesses: {rand_guesses}\n")
            return guesses[:num_guess]

        self.board_copy = copy.deepcopy(self.board_dict)
        while len(guesses) < 1:
            # just choose one random clue and dont guess more
            # select additional random clue

            gw, _ = random.choice(list(self.board_copy.items()))

            if gw not in prev_guesses:
                guesses.append(gw)
                rand_guesses += 1

        if self.log_file is not None:
            self.log_file.write(f"random_guesses: {rand_guesses}\n")
        return guesses[:num_guess]