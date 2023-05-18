import random

class RandomAI:
    def __init__(self):
        random.seed(72)
        self.board_words = []
    
    def load_dict(self, boardwords):
        self.board_words = boardwords.copy()

    def give_feedback(self, val, val2):
        pass

    def end_game(self, val):
        pass
