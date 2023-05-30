import sys

from utils.object_manager import ObjectManager
from run_tournament import RunTournament
from run_learning_experiment import RunLearningExperiment
from run_parameter_experiment import RunParameterExperiment
from utils.file_alignment_checker import FileAlignmentChecker

class FileRunner():
    def __init__(self):
        self.object_manager = ObjectManager()

    def run_tournament(self):
        run_tournament = RunTournament(self.object_manager)
        run_tournament.run()

    def run_parameter_experiment(self):
        run_parameter_experiment = RunParameterExperiment(self.object_manager)
        run_parameter_experiment.run()

    def run_learning_experiment(self):
        #There will be some sort of check to see if we just want to analyze results. If so, we do so here
        run_learning_experiment = RunLearningExperiment(self.object_manager)
        run_learning_experiment.run()
    
    def run_analysis(self):
        self.object_manager.results_analyzer.run_analysis()
    
    def check_files(self):
        file_alignment_checker = FileAlignmentChecker(self.object_manager)
        return file_alignment_checker.check_alignment()



if __name__=="__main__":

    #get arguments
    argv = sys.argv
    print(argv)
    # argv = ["not important", "DIST_ENS_WO", "0", "1"]

    file_runner = FileRunner()
    

    if len(argv) > 2:
        file_runner.object_manager.experiment_settings.config_setting = argv[1]
        file_runner.object_manager.experiment_settings.setup()
        if len(argv) > 3:
            file_runner.object_manager.experiment_settings.iteration_range = [int(argv[2]), int(argv[3])]
    else: 
        file_runner.object_manager.experiment_settings.config_setting = "DIST_ENS_WO"
        file_runner.object_manager.experiment_settings.setup()
    #now we reset the filepaths
        
    file_runner.object_manager.file_manager.generate_needed_filepaths()

    #at this point, we are good to go with our new settings

    if file_runner.object_manager.experiment_settings.experiment_type == file_runner.object_manager.experiment_types.PARAMETER_EXPERIMENT:
        file_runner.run_parameter_experiment()
    elif file_runner.object_manager.experiment_settings.experiment_type == file_runner.object_manager.experiment_types.LEARNING_EXPERIMENT:
        file_runner.run_learning_experiment()
    else:
        file_runner.run_tournament()

    print("all files aligned:", file_runner.check_files())
    file_runner.run_analysis()