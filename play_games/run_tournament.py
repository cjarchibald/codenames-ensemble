'''
This file will pair up bots and pass them into run_games. It will also make a cross table of results

authors: Spencer Brosnahan and Kyle Rogers
'''
import os
import sys
print(os.path.join(os.getcwd(), os.path.join("play_games", "utils")))
sys.path.insert(0, os.path.join(os.getcwd(), os.path.join("final_repo", "play_games")))

from run_games import RunGames

#Pass in settings object to other files and set the needed parameters

class RunTournament:
    def __init__(self, object_manager):
        self.object_manager = object_manager
        self.run_games = RunGames(object_manager)
        self.lower = None 
        self.upper = None 

    def run(self, lp=0, p=0):
        #Get needed information from the experiment_settings.py file
        codemasters = self.object_manager.experiment_settings.codemasters
        guessers = self.object_manager.experiment_settings.guessers
        n = self.object_manager.experiment_settings.n_games 
        is_learning_experiment = False

        if self.lower == None: 
            self.lower = 0
            self.upper = 0
            
        fi = (lp - self.lower)

        
        if self.object_manager.experiment_settings.experiment_type == self.object_manager.experiment_types.PARAMETER_EXPERIMENT:
            path = self.object_manager.file_paths_obj.round_log_filepaths[p][fi]
        else:
            path = self.object_manager.file_paths_obj.round_log_filepaths[fi]
        
        head = os.path.split(path)[0]
        if not os.path.exists(head):
            os.makedirs(head)
        self.object_manager.file_manager.ROUND_FILE = open(path, 'w+', encoding='utf8')

        if len(self.object_manager.file_paths_obj.learn_log_filepaths_cm) > 0:
            self.object_manager.file_manager.LEARN_LOG_FILE_CM = open(self.object_manager.file_paths_obj.learn_log_filepaths_cm[fi], 'w+', encoding='utf8')
            is_learning_experiment = True
        if len(self.object_manager.file_paths_obj.learn_log_filepaths_g) > 0:
            self.object_manager.file_manager.LEARN_LOG_FILE_G = open(self.object_manager.file_paths_obj.learn_log_filepaths_g[fi], 'w+', encoding='utf8')
            is_learning_experiment = True

        i = 0
        
        for b1 in codemasters:
            i += 1
            for b2 in guessers:
                #I need to check that at least one of the bots is ensemble if this is a learning experiment
                if is_learning_experiment:
                    #If neither bot is an ensemble, we don't play them together
                    if self.object_manager.bot_ai_types.get_bot_ai_type(b1) != self.object_manager.ai_types.DISTANCE_ENSEMBLE \
                        and self.object_manager.bot_ai_types.get_bot_ai_type(b1) != self.object_manager.ai_types.ASSOCIATOR_ENSEMBLE \
                        and self.object_manager.bot_ai_types.get_bot_ai_type(b2) != self.object_manager.ai_types.DISTANCE_ENSEMBLE \
                        and self.object_manager.bot_ai_types.get_bot_ai_type(b2) != self.object_manager.ai_types.ASSOCIATOR_ENSEMBLE \
                        and self.object_manager.bot_ai_types.get_bot_ai_type(b1) != self.object_manager.ai_types.RANDOM_ASSOCIATOR_ENSEMBLE \
                        and self.object_manager.bot_ai_types.get_bot_ai_type(b1) != self.object_manager.ai_types.RANDOM_DISTANCE_ENSEMBLE \
                        and self.object_manager.bot_ai_types.get_bot_ai_type(b2) != self.object_manager.ai_types.RANDOM_ASSOCIATOR_ENSEMBLE \
                        and self.object_manager.bot_ai_types.get_bot_ai_type(b2) != self.object_manager.ai_types.RANDOM_DISTANCE_ENSEMBLE:
                        continue
                self.object_manager.cond_print(f'Simulating {n} games with {b1} and {b2}', self.object_manager.experiment_settings.verbose_flag)
                self.run_games.run_n_games(int(n), b1, b2, lp, p)

        self.object_manager.file_manager.ROUND_FILE.close()

        if len(self.object_manager.file_paths_obj.learn_log_filepaths_cm) > 0:
            self.object_manager.file_manager.LEARN_LOG_FILE_CM.close()
        if len(self.object_manager.file_paths_obj.learn_log_filepaths_g) > 0:
            self.object_manager.file_manager.LEARN_LOG_FILE_G.close()


# if __name__=="__main__":
#     object_manager = ObjectManager()
#     tournament = RunTournament(object_manager)
#     tournament.run()