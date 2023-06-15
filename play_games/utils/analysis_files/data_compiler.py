import os
import shutil

class DataCompiler:
    def __init__(self, compiled_data_keys, compiled_data_stats, find_ensemble, file_paths_obj, create_path):
        self.compiled_data_keys = compiled_data_keys
        self.compiled_data_stats = compiled_data_stats
        self.find_ensemble = find_ensemble
        self.file_paths_obj = file_paths_obj
        self.create_path = create_path
    
    def get_image_paths(self, compiled_info, cm, g):
        data = compiled_info[cm][g]
        paths = []
        paths.extend(data[self.compiled_data_keys.ARM_WEIGHTS])
        paths.extend(data[self.compiled_data_keys.PERCENTAGES])
        for s in self.compiled_data_stats:
             paths.extend(data[self.compiled_data_keys.PERF_PROG][s])
             paths.extend(data[self.compiled_data_keys.PERF_PROG_SLIDE][s])
        
        for s in data[self.compiled_data_keys.FINAL_STAT_DIST]:
            if type(data[self.compiled_data_keys.FINAL_STAT_DIST][s]) == list:
                paths.extend([(e, s) for e in data[self.compiled_data_keys.FINAL_STAT_DIST][s]])
            else:
                paths.append((data[self.compiled_data_keys.FINAL_STAT_DIST][s], s))

        
        return paths

    
    def update_path(self, original_path, cm, g):
        direc, _ = os.path.split(original_path)
        direc = os.path.join(direc, cm, g)
        self.create_path(direc)
        return direc

    def get_text(self, compiled_info, cm, g):
        if self.compiled_data_keys.STAT_COMPARISON not in compiled_info[cm][g]:
            return None
        text = ""
        for k in compiled_info[cm][g][self.compiled_data_keys.STAT_COMPARISON]:
            text += k + ":\n"
            for e in compiled_info[cm][g][self.compiled_data_keys.STAT_COMPARISON][k]:
                text += f"{e}: {compiled_info[cm][g][self.compiled_data_keys.STAT_COMPARISON][k][e]}\n"
            text += "\n"
        return text


    def compile_data(self, compiled_info):
        #for each ensemble cm or g create a pdf with each slide being itself paired with all teammates
        cms = list(compiled_info.keys())
        gs = list(compiled_info[cms[0]].keys())

        ens_cm = self.find_ensemble(cms)
        ens_g = self.find_ensemble(gs)

        if ens_cm != None:
            #create a pdf document with guessers for the ensemble cm. Each should have its own slide 
            save_path = self.file_paths_obj.learn_experiment_analysis_filepath_cm

            for g in gs:
                self.create_compilation(*self.prep_data(compiled_info, ens_cm, g, save_path))

        if ens_g != None:
            save_path = self.file_paths_obj.learn_experiment_analysis_filepath_g
            
            for cm in cms:
                self.create_compilation(*self.prep_data(compiled_info, cm, ens_g, save_path))

    def prep_data(self, compiled_info, cm, g, save_path):
        title = cm + " with " + g
        image_paths = self.get_image_paths(compiled_info, cm, g)
        text = self.get_text(compiled_info, cm, g)
        output_path = self.update_path(save_path, cm, g)
        return title, image_paths, text, output_path
    
    def create_compilation(self, title, image_paths, text, output_path):
        #save all image paths to out path
        for p in image_paths:

            if type(p) == tuple:
                f = p[1] + ".jpg"
                p = p[0]
            else:
                d, f = os.path.split(p)

            dest = os.path.join(output_path, f)
            self.create_path(dest)
            shutil.copy2(p, dest)
        
        #create a text file
        if text != None:
            sp = os.path.join(output_path, "stat-comp.txt")
            with open(sp, "w+") as f:
                f.write(text)
