import scipy.spatial.distance
import numpy as np
import itertools

import ai_components.vector_baseline_components.vector_utils as VectorUtils
from ai_components.ai_components_utils import arr_not_in_word

class VectorBaselineCodemaster():

    def __init__(self, tolerance, first_vecs_path, second_vecs_path, out_file=None):

        self.out_file = out_file
        self.first_vecs = VectorUtils.load_vectors(first_vecs_path)
        self.cm_wordlist = set(self.first_vecs.keys()).copy()
        
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

    def generate_clue(self, player_words, prev_clues, opponent_words, assassin_word, bystander_words):

        cos_dist = scipy.spatial.distance.cosine
        red_words = player_words
        bad_words = opponent_words + [assassin_word] + bystander_words

        all_vectors = self.all_vectors
        bests = {}

        if not self.bad_word_dists:
            self.bad_word_dists = {}
            for word in bad_words:
                self.bad_word_dists[word] = {}
                for val in self.cm_wordlist:
                    b_dist = cos_dist(VectorUtils.concatenate(val, all_vectors), VectorUtils.concatenate(word, all_vectors))
                    self.bad_word_dists[word][val] = b_dist

            self.red_word_dists = {}
            for word in red_words:
                self.red_word_dists[word] = {}
                for val in self.cm_wordlist:
                    b_dist = cos_dist(VectorUtils.concatenate(val, all_vectors), VectorUtils.concatenate(word, all_vectors))
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
                
                for word in self.cm_wordlist:

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
                dist = cos_dist(VectorUtils.concatenate(word, all_vectors), VectorUtils.concatenate(combined_clue, all_vectors))
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
            self.out_file.write(f"original original threshold: {self.tolerance}\n")
            self.out_file.write(f"original new threshold: {chosen_clue[3]}\n")
            self.out_file.write(f"original worst red: {chosen_worst}\n")

        targets = list(bests[chosen_num][0])
        return chosen_clue[1], targets  # [li[0][3], 1]



    