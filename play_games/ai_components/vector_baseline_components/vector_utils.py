import numpy as np

class VectorUtils:
    def load_vectors(self, path):
        with open(path, encoding="utf-8") as infile:
            vecs = {}
            for line in infile:
                line = line.rstrip().split(' ')
                vecs[line[0]] = np.array([float(n) for n in line[1:]])
            return vecs

    def load_word_list(self, path):
        wordlist = []
        in_file = open(path, "r")
        for line in in_file:
            wordlist.append(line.strip())
        in_file.close()
        
        return wordlist

    def concatenate(self, word, wordvecs):
        concatenated = wordvecs[0][word]
        for vec in wordvecs[1:]:
            concatenated = np.hstack((concatenated, vec[word]))
        return concatenated