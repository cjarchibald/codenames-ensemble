
class DataParser:
    def __init__(self, file_paths_obj, round_log_parser, learn_log_parser, bot_ai_types, ai_types, stat_dict_keys, types, save_json, load_json):
        self.file_paths_obj = file_paths_obj
        self.round_log_parser = round_log_parser
        self.learn_log_parser = learn_log_parser
        self.bot_ai_types = bot_ai_types
        self.ai_types = ai_types
        self.stat_dict_keys = stat_dict_keys
        self.types = types 
        self.save_json = save_json
        self.load_json = load_json


    def parse_data(self, round_logs, learn_logs_cm, learn_logs_g, parsed_data_filepaths):

        #Compile the needed filepaths to parse

        #All experiments parse the round logs
        parsed_round_log_data = self.round_log_parser.run_parser(round_logs)

        #If it is a learning experiment, then we need to parse the learn logs as well
        if len(learn_logs_cm) != 0:
            parsed_learn_log_data_cm = self.learn_log_parser.run_parser(learn_logs_cm)
        if len(learn_logs_g) != 0:
            parsed_learn_log_data_g = self.learn_log_parser.run_parser(learn_logs_g)

        #Save the data
        final_dict = {}
        for counter, filepath in enumerate(parsed_data_filepaths):
            try:
                merged_dict = parsed_round_log_data[counter]
                if len(learn_logs_cm) != 0:
                    llcm_dict = parsed_learn_log_data_cm[counter]
                    self.merge_data(merged_dict, llcm_dict, self.types.CM)
                if len(learn_logs_g) != 0:
                    llg_dict = parsed_learn_log_data_g[counter]
                    self.merge_data(merged_dict, llg_dict, self.types.G)

                final_dict[counter] = merged_dict

                self.save_json(merged_dict, filepath)

            except:
                continue

        return final_dict

    def merge_data(self, merged_dict, learning_dict, type):
        for cm in merged_dict:
            for g in merged_dict[cm]:
                if type == self.types.CM and (self.ai_types.DISTANCE_ENSEMBLE == self.bot_ai_types.get_bot_ai_type(cm)):
                    merged_dict[cm][g][self.stat_dict_keys.CM_LEARN_STATS] = learning_dict[g]
                elif type == self.types.G and (self.ai_types.DISTANCE_ENSEMBLE == self.bot_ai_types.get_bot_ai_type(g)):
                    merged_dict[cm][g][self.stat_dict_keys.G_LEARN_STATS] = learning_dict[cm]

    def load_parsed_data(self):
        parsed_data = {}
        counter = 0
        for filepath in self.file_paths_obj.parsed_data_filepaths:
            try:
                parsed_data[counter] = self.load_json(filepath)
            except:
                counter += 1
                continue
            counter += 1
        return parsed_data