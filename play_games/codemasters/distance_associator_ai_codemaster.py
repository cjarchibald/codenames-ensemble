from ai_components.associator_ai_components.distance_associator import DistanceAssociator
import numpy as np

class DistanceAssociatorAICodemaster(DistanceAssociator):
    def __init__(self):
        self.association_location_dict = {}
        self.closest_bad_words = {}
    
    def initialize(self, settings_obj):
        super().__init__(settings_obj.N_ASSOCIATIONS, settings_obj.CONSTRUCTOR_PATHS[0], settings_obj.CONSTRUCTOR_PATHS[1])
    
    def generate_clue(self, player_words, prev_clues, opponent_words, assassin_word, bystander_words):
        # find max occurrence - this will be the clue (see fixme comment above)
        self.association_location_dict = self.find_common_word_associations(player_words) 
        self.filter_unwanted_clues(opponent_words + bystander_words, assassin_word)
        clue, target_words = self.find_best_clue()


        return clue, target_words
    


    def find_best_clue(self): 
        #We must first order our dictionary
        # Primarily by number of associated words, secodarily by sum of targets
        all_pos_clues = []
        for pos_clue in self.association_location_dict.keys():
            associated_boardwords = self.association_location_dict[pos_clue].keys()
            num_targets = len(associated_boardwords)
            total_distance = 0
            for word in associated_boardwords:
                total_distance += self.association_location_dict[pos_clue][word]
            all_pos_clues.append((pos_clue, num_targets, total_distance))

        sorted_clues = sorted(all_pos_clues, key=lambda x: (-x[1], x[2]))
        clue = sorted_clues[0][0]
        targets = list(self.association_location_dict[clue].keys())
        return clue, targets
    
    def find_bad_distances(self, bad_words):
        bad_dists_dict = {}
        for pos_clue in self.association_location_dict.keys():
            worst_bad = np.inf
            worst_word = None
            for word in bad_words:
                curr_dist = self.calculate_dist(pos_clue, word)
                if curr_dist < worst_bad:
                    worst_bad = curr_dist
                    worst_word = word
            
            bad_dists_dict[pos_clue] = worst_bad
        return bad_dists_dict


    
    
    def filter_unwanted_clues(self, opponent_words, assassin_word):
        #we filter out unwanted words (prev_clues and any association that has the assassin within the assassin_threshold and a blue word within
        # the blue_word_threshold)

        bad_words = opponent_words + [assassin_word]
        self.closest_bad_words = self.find_bad_distances(bad_words)
        
        for pos_clue in self.association_location_dict.keys():
            associated_board_words = self.association_location_dict[pos_clue].keys()
            words_to_keep = {}
            for word in associated_board_words:
                cos_dist = self.association_location_dict[pos_clue][word]
                closest_bad = self.closest_bad_words[pos_clue]
                if cos_dist < closest_bad:
                    words_to_keep[word] = cos_dist
            self.association_location_dict[pos_clue] = words_to_keep