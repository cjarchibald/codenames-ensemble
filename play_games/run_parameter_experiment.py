from run_learning_experiment import RunLearningExperiment

class RunParameterExperiment:
    def __init__(self, object_manager):
        self.object_manager = object_manager
        self.run_learning_experiment = RunLearningExperiment(object_manager)

    def run(self):
        variables = self.object_manager.experiment_settings.independent_variable

        for i in range(len(variables)):
            self.run_learning_experiment.run(i)