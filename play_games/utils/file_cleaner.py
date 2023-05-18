import os

class FileCleaner:
    def __init__(self, object_manager):
        self.object_manager = object_manager

    def clean_learn_logs(self):
        cm_learn_logs = self.object_manager.file_paths_obj.learn_log_filepaths_cm 
        g_learn_logs = self.object_manager.file_paths_obj.learn_log_filepaths_g

        #clean all of the cm learn logs 
        
        for l in cm_learn_logs:
            new_lines = []
            count = 0
            try:
                with open(l, 'r') as f:
                    for line in f:
                        elements = line.split(' ')
                        if elements[0] == "STARTING":
                            count += 1 
                        if  count > 18:
                            break
                        #otherwise we write it to our new file 
                        new_lines.append(line)
            except:
                continue

            #swithch this out for the same file name 
            with open(l, 'w+') as f:
                for line in new_lines:
                    f.write(line)
        
        #now we do a similar thing for g 
        
        for l in g_learn_logs:
            new_lines = []
            count = 0 
            skip = False 
            try:
                with open(l, 'r') as f:
                    for line in f:
                        elements = line.split(' ')
                        if elements[0] == "STARTING" and skip == False:
                            skip = True
                            count += 1 
                        elif elements[0] == "STARTING" and skip == True:
                            skip = False

                        if  count % 2 == 0:
                            continue
                        #otherwise we write it to our new file 
                        new_lines.append(line)
            except:
                continue

            with open(l, 'w+') as f:
                for line in new_lines:
                    f.write(line)
    
    def delete_small_files(self):
        round_logs_dir = self.object_manager.file_paths_obj.round_logs_dir_path
        learn_logs_dir = self.object_manager.file_paths_obj.learn_logs_dir_path

        #loop through all of the round logs and delete all of the files less than 1 MB 
        for log in os.listdir(round_logs_dir):
            p = os.path.join(round_logs_dir, log)
            file_size = os.path.getsize(p)
            if file_size < 10000000: #megabyte 
                os.remove(p)
            
        
        # for log in os.listdir(learn_logs_dir):
        #     p = os.path.join(learn_logs_dir, log)
        #     file_size = os.path.getsize(p)
        #     if file_size < 1000000: 
        #         os.remove(p)