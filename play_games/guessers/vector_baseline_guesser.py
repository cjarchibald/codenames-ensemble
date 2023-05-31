from ai_components.vector_baseline_components.vector_utils import VectorUtils
import scipy.spatial.distance

import numpy as np

class VectorBaselineGuesser():
    def __init__(self):
        self.vector_utils = VectorUtils()

    def initialize(self, bot_settings_obj):
        if type(bot_settings_obj.CONSTRUCTOR_PATHS) == list:
            first_vecs_path = bot_settings_obj.CONSTRUCTOR_PATHS[0]
            second_vecs_path = bot_settings_obj.CONSTRUCTOR_PATHS[1]
        else:
            first_vecs_path = bot_settings_obj.CONSTRUCTOR_PATHS
            second_vecs_path = None

        self.first_vecs = self.vector_utils.load_vectors(first_vecs_path)
        self.second_vectors = {}
        if second_vecs_path:
            self.second_vectors = self.vector_utils.load_vectors(second_vecs_path)
        self.num = 0
    
    def guess_clue(self, clue, num_guess, prev_guesses):
        sorted_words = self.compute_distance(clue, [w for w in self.board_words if w not in prev_guesses])
        guesses = []
        for i in range(len(sorted_words[:num_guess])):
            guesses.append(sorted_words[i][1])
        return guesses

    def load_dict(self, words):
        self.board_words = words.copy()


    def compute_distance(self, clue, board):
        w2v = []
        if self.second_vectors:
            all_vectors = (self.second_vectors, self.first_vecs,)
        else:
            all_vectors = (self.first_vecs,)

        for word in board:
            w2v.append((scipy.spatial.distance.cosine(self.concatenate(clue, all_vectors),
                                                        self.concatenate(word.lower(), all_vectors)), word))

        w2v = list(sorted(w2v))
        return w2v


    def concatenate(self, word, wordvecs):
        concatenated = wordvecs[0][word]
        for vec in wordvecs[1:]:
            concatenated = np.hstack((concatenated, vec[word]))
        return concatenated

    def give_feedback(self, val1, val2):
        pass
    
    def end_game(self, val):
        pass