"""
This file does the actual game simulation and logs the stats and returns some to run_n_games. 

authors: Kim et al., Spencer Brosnahan, and Dallin Hunter
"""

import random
import time
import enum
import sys

class GameCondition(enum.Enum):
    """Enumeration that represents the different states of the game"""
    HIT_RED = 0
    HIT_BLUE = 1
    HIT_ASSASSIN = 2
    LOSS = 3
    WIN = 4
    CONTINUE = 5


class Game:
    """Class that setups up game details and calls Guesser/Codemaster pair to play the game
    """

    def __init__(self, btype1, btype2, codemaster, guesser, board_words, seed, object_manager):

        self.object_manager = object_manager
        self.btype1 = btype1
        self.btype2 = btype2
        self.codemaster = codemaster
        self.guesser = guesser
        self.words_on_board = board_words
        self.seed = seed
        self.board_words = board_words.copy()
        self.do_print = object_manager.experiment_settings.print_boards
        self.game_time = 0

        self.game_start_time = time.time()


        random.seed(self.seed)

        self.total_red_words = 9
        self.total_blue_words = self.total_red_words - 1
        self.total_bystanders = 25 - self.total_blue_words - self.total_red_words - 1  # minus one for the assassin
        self.key_grid = ['Red'] * self.total_red_words + ['Blue'] * self.total_blue_words + [
            'Bystander'] * self.total_bystanders + ['Assassin']

        random.shuffle(self.key_grid)

        self.red_words = []
        self.red_guesses = []
        self.clues_used = []
        self.blue_words = []
        self.blue_guesses = []
        self.assassin_word = ""
        self.bystander_words = []
        self.bystander_guesses = []

        self.assign_words()

        self.score = 0
        self.targets_guessed = 0
        self.opponent_words_guessed = 0
        self.game_won = 0
        self.assassin_guessed = False

    def assign_words(self):
        for i in range(len(self.words_on_board)):
            word = self.words_on_board[i]
            affiliation = self.key_grid[i]
            if affiliation == 'Red':
                self.red_words.append(word)
            elif affiliation == 'Blue':
                self.blue_words.append(word)
            elif affiliation == 'Bystander':
                self.bystander_words.append(word)
            else:
                self.assassin_word = word



    def _display_board_codemaster(self):
        """prints out board with color-paired words, only for codemaster, color && stylistic"""
        if self.do_print:
            original_stdout = sys.stdout
            sys.stdout = self.object_manager.file_manager.ROUND_FILE
            print(str.center(
                "_____________________________________BOARD_____________________________________\n", 60))
            counter = 0
            for i in range(len(self.words_on_board)):
                if counter >= 1 and i % 5 == 0:
                    print("\n")
                if self.key_grid[i] == 'Red':
                    print(str.center(self.words_on_board[i], 15), " ", end ='')
                    counter += 1
                elif self.key_grid[i] == 'Blue':
                    print(str.center(self.words_on_board[i], 15), " ", end='')
                    counter += 1
                elif self.key_grid[i] == 'Bystander':
                    print(str.center(self.words_on_board[i], 15), " ", end='')
                    counter += 1
                else:
                    print(str.center(self.words_on_board[i], 15), " ", end='')
                    counter += 1
            print(str.center(
                            "\n_______________________________________________________________________________", 60))
            print("\n")
            sys.stdout = original_stdout


    def get_words_on_board(self):
        """Return the list of words that represent the board state"""
        return self.words_on_board

    def _accept_guess(self, guess_index, guess):
        """Function that takes in an int index called guess to compare with the key grid
        CodeMaster will always win with Red and lose if Blue =/= 7 or Assassin == 1

        1 loss, 2 win, 0 continue
        0 red, 1 blue, 2 bystander, 3 assassin
        first end status, second word type
        """

        if self.key_grid[guess_index] == "Red":
            self.red_guesses.append(self.words_on_board[guess_index])
            self.targets_guessed += 1
            self.words_on_board[guess_index] = "*Red*"
            self.object_manager.file_manager.ROUND_FILE.write("correct guess\n")
            if self.words_on_board.count("*Red*") >= self.total_red_words:
                self.object_manager.file_manager.ROUND_FILE.write("game won\n")
                self.guesser.give_feedback(2, 0)
                return GameCondition.WIN
            self.guesser.give_feedback(0, 0)
            return GameCondition.HIT_RED

        elif self.key_grid[guess_index] == "Blue":
            self.opponent_words_guessed += 1
            self.blue_guesses.append(self.words_on_board[guess_index])
            self.words_on_board[guess_index] = "*Blue*"
            self.object_manager.file_manager.ROUND_FILE.write("incorrect guess\n")
            if self.words_on_board.count("*Blue*") >= self.total_blue_words:
                self.object_manager.file_manager.ROUND_FILE.write("game lost\n")
                self.guesser.give_feedback(1, 1)
                return GameCondition.LOSS
            else:
                self.guesser.give_feedback(0, 1)
                return GameCondition.CONTINUE

        elif self.key_grid[guess_index] == "Assassin":
            self.assassin_guessed = True
            self.words_on_board[guess_index] = "*Assassin*"
            self.object_manager.file_manager.ROUND_FILE.write("assassin guessed\ngame lost\n")
            self.guesser.give_feedback(1, 3)
            return GameCondition.LOSS

        else:
            self.bystander_guesses.append(self.words_on_board[guess_index])
            self.words_on_board[guess_index] = "*Bystander*"
            self.object_manager.file_manager.ROUND_FILE.write("bystander guessed\n")
            self.guesser.give_feedback(0, 2)
            return GameCondition.CONTINUE

    
    def get_game_stats(self):

        if self.game_won == 0:
            self.score = 25
        else:
            self.score = len(self.clues_used)
        
        self.game_time = self.game_end_time - self.game_start_time
        



    def run(self):
        """Function that runs the codenames game between codemaster and guesser"""
        game_string = f"CODEMASTER: {self.btype1}\nGUESSER: {self.btype2}\n"
        self.object_manager.file_manager.ROUND_FILE.write(game_string)

        self._display_board_codemaster()

        self.object_manager.file_manager.ROUND_FILE.write(f"seed: {self.seed}\n")
        self.object_manager.file_manager.ROUND_FILE.write("board_words: " + str(self.board_words) + '\n\n')

        game_condition = GameCondition.HIT_RED
        round = 1

 
        while game_condition != GameCondition.LOSS and game_condition != GameCondition.WIN:
            # # Creating game that will run only once clue/guess pair

            # board setup and display
            words_in_play = self.get_words_on_board()
            
            self.object_manager.file_manager.ROUND_FILE.write(f"round: {round}\n")
            round += 1

            # codemaster gives clue & number here
            clue_giving_start = time.time()
            red_words_left = [w for w in self.red_words if w not in self.red_guesses]
            blue_words_left = [w for w in self.blue_words if w not in self.blue_guesses]
            bystander_words_left = [w for w in self.bystander_words if w not in self.bystander_guesses]

            self.object_manager.file_manager.ROUND_FILE.write("red_words_left: " + str(red_words_left) + '\n')
            self.object_manager.file_manager.ROUND_FILE.write("blue_words_left: " + str(blue_words_left) + '\n')
            self.object_manager.file_manager.ROUND_FILE.write("bystander_words_left: " + str(bystander_words_left) + '\n')
            self.object_manager.file_manager.ROUND_FILE.write("assassin_word: " + self.assassin_word + '\n')
            self.object_manager.file_manager.ROUND_FILE.write(f"num_red_words_left: {len(red_words_left)}\n")
            clue, targets = self.codemaster.generate_clue(red_words_left, self.clues_used,blue_words_left, self.assassin_word, 
                bystander_words_left)                                                   
            clue_giving_end = time.time()
            clue_giving_time = clue_giving_end - clue_giving_start

            self.clues_used.append(clue)

            self.object_manager.file_manager.ROUND_FILE.write(f"clue: {clue}\ntargets: {targets}\nnum_targets: {len(targets)}\n")

            clue_num = len(targets)

            guess_num = 1
            clue_num = int(clue_num)

            guessing_start = time.time()
            guesses = self.guesser.guess_clue(clue, clue_num, self.red_guesses + self.blue_guesses + self.bystander_guesses)
            guessing_end = time.time()
            guessing_time = guessing_end - guessing_start

            self.object_manager.file_manager.ROUND_FILE.write(f"clue_generation_time: {clue_giving_time}\nguess_generation_time: {guessing_time}\n")
            self.object_manager.file_manager.ROUND_FILE.write(f"guesses: {guesses}\n")

            game_condition = GameCondition.HIT_RED
            for guess_answer in guesses:
                if guess_num <= clue_num and game_condition == GameCondition.HIT_RED:

                    self.object_manager.file_manager.ROUND_FILE.write(f"guess: {guess_answer}\n")

                    guess_answer_index = words_in_play.index(
                        guess_answer.lower().strip())
                    game_condition = self._accept_guess(guess_answer_index, guess_answer)

                    if game_condition == GameCondition.HIT_RED:
                        self.codemaster.give_feedback(guess_answer, 0)
                        self._display_board_codemaster()
                        guess_num += 1
                        continue

                    # if guesser selected a civilian or a blue-paired word
                    elif game_condition == GameCondition.CONTINUE:
                        self.codemaster.give_feedback(guess_answer, 0)
                        self._display_board_codemaster()
                        break

                    elif game_condition == GameCondition.LOSS:
                        self.codemaster.give_feedback(guess_answer, 1)
                        self.game_end_time = time.time()
                        self._display_board_codemaster()

                    elif game_condition == GameCondition.WIN:
                        self.codemaster.give_feedback(guess_answer, 2)
                        self.game_end_time = time.time()
                        self._display_board_codemaster()
                        self.game_won = 1
                else:
                    break
        self.object_manager.file_manager.ROUND_FILE.write(f"num_actual_guesses: {guess_num}\n")
        self.object_manager.file_manager.ROUND_FILE.write('\n')