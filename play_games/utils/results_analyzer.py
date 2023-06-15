import numpy as np
import os, json, copy, joblib  


'''
This class is responsible for the stats analysis flow

parse data -> save to file -> process data -> save to file -> visual
'''

class ResultsAnalyzer:
    def __init__(self, experiment_settings, file_paths_obj, experiment_types, data_parser, data_processor, data_visualizer):

        self.experiment_settings = experiment_settings
        self.file_paths_obj = file_paths_obj
        self.experiment_types = experiment_types

        self.data_parser = data_parser
        self.data_processer = data_processor
        self.data_visualizer = data_visualizer

        self.use_preloaded_parsed = False
        self.use_preloaded_processed = False
        self.use_preloaded_visualized = False
        
        self.data_visualizer.figure_creator.fig = not self.use_preloaded_visualized


    def run_analysis(self):
        
        if self.experiment_settings.experiment_type == self.experiment_types.LEARNING_EXPERIMENT:

            round_logs = self.file_paths_obj.round_log_filepaths
            learn_logs_cm = self.file_paths_obj.learn_log_filepaths_cm
            learn_logs_g = self.file_paths_obj.learn_log_filepaths_g
            parsed_data_filepaths = self.file_paths_obj.parsed_data_filepaths
            processed_data_filepaths = self.file_paths_obj.processed_data_filepaths

            if not self.use_preloaded_parsed:
                parsed_data = self.data_parser.parse_data(round_logs, learn_logs_cm, learn_logs_g, parsed_data_filepaths)
            else:
                parsed_data = self.data_parser.load_parsed_data()
            if not self.use_preloaded_processed:
                processed_data = self.data_processer.process_data(parsed_data, processed_data_filepaths)
            else:
                processed_data = self.data_processer.load_processed_data()

            self.data_visualizer.visualize_data(processed_data)

        elif self.experiment_settings.experiment_type == self.experiment_types.PARAMETER_EXPERIMENT:
            
            final_processed_data = {}
            for i in range(len(self.experiment_settings.independent_variable)):

                round_logs = self.file_paths_obj.round_log_filepaths[i]

                parsed_data_filepaths = self.file_paths_obj.parsed_data_filepaths[i]
                
                processed_data_filepaths = self.file_paths_obj.processed_data_filepaths[i]

                if not self.use_preloaded_parsed:
                    parsed_data = self.data_parser.parse_data(round_logs, [], [], parsed_data_filepaths)
                else:
                    parsed_data = self.data_parser.load_parsed_data(None, None, None, parsed_data_filepaths)
                if not self.use_preloaded_processed:
                    processed_data = self.data_processer.process_data(parsed_data, processed_data_filepaths)
                else:
                    processed_data = self.data_processer.load_processed_data(None, processed_data_filepaths)

                final_processed_data[i] = processed_data

            if not self.use_preloaded_visualized:
                self.data_visualizer.visualize_data(final_processed_data)

        else: #this is a tournament
            round_logs = self.file_paths_obj.round_log_filepaths
            parsed_data_filepaths = self.file_paths_obj.parsed_data_filepaths
            processed_data_filepaths = self.file_paths_obj.processed_data_filepaths

            if not self.use_preloaded_parsed:
                parsed_data = self.data_parser.parse_data(round_logs, [], [], parsed_data_filepaths)
            else:
                parsed_data = self.data_parser.load_parsed_data()
            if not self.use_preloaded_processed:
                processed_data = self.data_processer.process_data(parsed_data, processed_data_filepaths)
            else:
                processed_data = self.data_processer.load_processed_data()

            if not self.use_preloaded_visualized:
                self.data_visualizer.visualize_data(processed_data)