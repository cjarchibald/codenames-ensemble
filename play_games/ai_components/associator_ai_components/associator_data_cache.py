'''
This file will contain associations from the json file. You will pass in a filepath

authors: Spencer Brosnahan and Kyle Rogers
'''

import json

class AssociatorDataCache:
    def __init__(self, filepath):
        self.filepath = filepath
        self.associations = {}
        self.wordlist = []
    
    def load_cache(self,n):
        with open(self.filepath) as f:
            self.associations = json.load(f)
        for key in self.associations.keys():
            new_list = []
            old_list = self.associations[key]
            new_list = old_list[:n].copy()
            self.associations[key] = new_list
            self.wordlist.append(key)
    
    def get_associations(self, word):
        return self.associations[word]
    
    def get_wordlist(self):
        return self.wordlist
    
    
    def get_ext_associations(self, word):
        new_associations = []
        original_associations = self.associations[word]
        for w in original_associations:
            if w not in new_associations:
                new_associations.append(w)
            word_associations = self.associations[w]
            new_word = word_associations[0]
            if new_word not in new_associations:
                new_associations.append(new_word)
            
        return new_associations