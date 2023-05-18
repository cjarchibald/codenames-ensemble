import scipy.spatial.distance as dist

from ai_components.associator_ai_components.associator_data_cache import AssociatorDataCache
from ai_components.vector_baseline_components.vector_utils import VectorUtils

class DistanceAssociator:
    def __init__(self, n, path, vector_path):
        self.vector_utils = VectorUtils()
        self.datacache = AssociatorDataCache(path)
        self.datacache.load_cache(n)
        self.vectors = self.vector_utils.load_vectors(vector_path)
        self.board_dict = {}
        self.boardwords = []
    
    def load_dict(self, boardwords):
        self.boardwords = boardwords.copy()
        self.board_dict.clear()
        for word in boardwords.copy():
            self.board_dict[word] = self.datacache.get_associations(word)

    def give_feedback(self, guess, end_status):
        pass
    
    def calculate_dist(self, w1, w2):
        return dist.cosine(self.vectors[w1], self.vectors[w2])

    def find_common_word_associations(self, input_words):
        #we create a dictionary of all associated words as keys and the word that they are associated to as a second key and 
        association_location_dict = {}
        for word in input_words:
            associations = self.board_dict[word]
            for association in associations:
                if association not in input_words and association not in self.board_dict.keys():
                    if association in association_location_dict.keys():
                        association_location_dict[association][word] = self.calculate_dist(association, word)
                    else:
                        association_location_dict[association] = {}
                        association_location_dict[association][word] = self.calculate_dist(association, word)
        return association_location_dict