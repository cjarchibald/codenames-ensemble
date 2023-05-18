import scipy.spatial.distance
import numpy as np
import itertools

import ai_components.vector_baseline_components.vector_utils as VectorUtils
from ai_components.associator_ai_components.associator_data_cache import AssociatorDataCache
from ai_components.ai_components_utils import arr_not_in_word

class OptimizedVectorBaselineCodemaster():

    def __init__(self, n_associations, tolerance, associations_path, first_vecs_path, second_vecs_path, out_file=None):

        self.out_file = out_file

        self.first_vecs = VectorUtils.load_vectors(first_vecs_path)
        self.datacache = AssociatorDataCache(associations_path)
        self.datacache.load_cache(n_associations)
        
        if second_vecs_path:
            self.second_vectors = VectorUtils.load_vectors(second_vecs_path)
            self.all_vectors = (self.first_vecs, self.second_vectors)           
        else:
            self.all_vectors = (self.first_vecs,)

        self.bad_word_dists = None
        self.red_word_dists = None

        self.tolerance = tolerance

    def load_dict(self, board_words):
        self.bad_word_dists = None
        self.red_word_dists = None
        self.board_words = board_words

    def give_feedback(self, val):
        pass
    
    def get_possible_clue_set(self, red_words):
        possible_clues = set()
        for word in red_words:
            associations = self.datacache.get_associations(word)
            for association in associations:
                possible_clues.add(association)
        return possible_clues

    def generate_clue(self, player_words, prev_clues, opponent_words, assassin_word, bystander_words):

        cos_dist = scipy.spatial.distance.cosine
        red_words = player_words
        bad_words = opponent_words + [assassin_word] + bystander_words
        possible_clue_set = self.get_possible_clue_set(red_words)

        all_vectors = self.all_vectors
        bests = {}

        if not self.bad_word_dists:
            self.bad_word_dists = {}
            for word in bad_words:
                self.bad_word_dists[word] = {}
                for val in possible_clue_set:
                    b_dist = cos_dist(self.concatenate(val, all_vectors), self.concatenate(word, all_vectors))
                    self.bad_word_dists[word][val] = b_dist

            self.red_word_dists = {}
            for word in red_words:
                self.red_word_dists[word] = {}
                for val in possible_clue_set:
                    b_dist = cos_dist(self.concatenate(val, all_vectors), self.concatenate(word, all_vectors))
                    self.red_word_dists[word][val] = b_dist

        else:
            to_remove = set(self.bad_word_dists) - set(bad_words)
            for word in to_remove:
                del self.bad_word_dists[word]
            to_remove = set(self.red_word_dists) - set(red_words)
            for word in to_remove:
                del self.red_word_dists[word]

        for clue_num in range(1, 3 + 1):
            best_per_dist = np.inf
            best_per = ''
            best_red_word = ''
            worst_per_dist = np.inf
            for red_word in list(itertools.combinations(red_words, clue_num)):
                best_word = ''
                best_dist = np.inf
                for word in possible_clue_set:
                    if not arr_not_in_word(word, red_words + bad_words):
                        continue

                    bad_dist = np.inf
                    worst_bad = ''
                    for bad_word in self.bad_word_dists:
                        if self.bad_word_dists[bad_word][word] < bad_dist:
                            bad_dist = self.bad_word_dists[bad_word][word]
                            worst_bad = bad_word
                    worst_red = 0
                    for red in red_word:
                        dist = self.red_word_dists[red][word]
                        if dist > worst_red:
                            worst_red = dist

                    if worst_red < best_dist and worst_red < bad_dist:
                        best_dist = worst_red
                        best_word = word
                        # print(worst_red,red_word,word)

                        if best_dist < best_per_dist:
                            best_per_dist = best_dist
                            best_per = best_word
                            best_red_word = red_word
                            worst_per_dist = bad_dist #the closest bad word distance to any of our target words. All target word distances are smaller than this

            bests[clue_num] = (best_red_word, best_per, best_per_dist, worst_per_dist)

        print("BESTS: ", bests)
        li = []
        pi = []
        chosen_clue = bests[1]
        chosen_num = 1
        chosen_worst = np.inf
        for clue_num, clue in bests.items():
            best_red_word, combined_clue, combined_score, closest_bad_word = clue
            worst = -np.inf
            best = np.inf
            worst_word = ''
            for word in best_red_word:
                dist = cos_dist(self.concatenate(word, all_vectors), self.concatenate(combined_clue, all_vectors))
                if dist > worst:
                    worst_word = word
                    worst = dist
                if dist < best:
                    best = dist
            if worst < self.tolerance and worst != -np.inf:
                print(worst, chosen_clue, chosen_num)
                chosen_worst = worst
                chosen_clue = clue
                chosen_num = clue_num

            li.append((worst / best, best_red_word, worst_word, combined_clue,
                       combined_score, combined_score ** len(best_red_word)))

        if chosen_clue[2] == np.inf:
            chosen_clue = ('', li[0][3], 0)
            chosen_num = 1
        # print("LI: ", li)
        # print("The clue is: ", li[0][3])
        print('chosen_clue is:', chosen_clue)
        # return in array styled: ["clue", number]

        #Addition
        if self.out_file:
            self.out_file.write(f"optimized original threshold: {self.tolerance}\n")
            self.out_file.write(f"optimized new threshold: {chosen_clue[3]}\n")
            self.out_file.write(f"optimized worst red: {chosen_worst}\n")

        targets = list(bests[chosen_num][0])
        return chosen_clue[1], targets  # [li[0][3], 1]


    def combine(self, words, wordvecs):
        factor = 1.0 / float(len(words))
        new_word = self.concatenate(words[0], wordvecs) * factor
        for word in words[1:]:
            new_word += self.concatenate(word, wordvecs) * factor
        return new_word

    def concatenate(self, word, wordvecs):
        concatenated = wordvecs[0][word]
        for vec in wordvecs[1:]:
            concatenated = np.hstack((concatenated, vec[word]))
        return concatenated
    