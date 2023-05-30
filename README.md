# Codenames Ensemble

This is the code used in *Adapting to Teammates in a Cooperative Language Game* by Christopher Archibald and Spencer Brosnahan

## Overview 

This repository contains everything needed to replicate our experiments. All you need to do is clone the repo and set up the environment using the .yml file in the repo and you're done! 

## Setting Up the Environment

run the following command 

```
conda env create -f environment.yml
``` 

## Project Structure 

Here, I will walk through the sub-directories in the repository and briefly explain what each is for. 

'data_objects' contains two sub-directories. 

- The first is 'associator_objects'. This contains the pre-computed association lists for all the codenames board words. These are used by our Distance Associator bots. 

- The secode is 'models'. This contains the model used to compute the CoLT score in our ACE framework. 

'play_games' is where all the logic for the experiments and the bots is contained. 

- 'file_runner.py' is the file used to kick off an experiment. You can either start an experiment from the command line or from the file itself. 

- 'run_learning_experment.py' and 'run_parameter_experiment.py' are where the the logic for the two different kinds of experiments are. A learning experiments is used to analyze how our ACE bots learn while a parameter experiment is used to analyze how different parameters affect average performance. More on that later, though. 

- Every experiment runs tournaments. This logic is in 'run_tournament.py'

- Every tournament runs n games for each team. This logic is in "run_games.py'

- The logic for an individual game is in 'game.py' 

    - 'utils' contains all of the objects and scripts used for stat tracking/analysis, bot instantiation, experiment setup, and dynamic object management. 

        - 'analysis_files' contains 'analysis_utils' which just contains objects and functions used multiple times in 'results_analyzer.py'. It also contains the 'parsers' directory which contains parsers for learn logs and round logs. 

'raw_data' is where all the wordlists and word embeddings are kept. 

'stats' is where all things relating to bot statistics in gameplay are kept. 

- 'comparison_files' contains 'comparison_objects' which is where we keep files that have stats we can compare our bot performance against. 

- 'saved_results' is where all the experiment results are kept. 
    
    - There are subdirectories for the results of learning experiments and parameter experiments separately

    - There are different directories to store the data for each step in the data processing pipeline

        - 'raw_data' contains the round and learn logs from the experiments
        
        - 'parsed_data' contains the raw info from the round and learn logs

        - 'processed_data' contains more useful stats computed from parsed data. 

        - 'visualizations' contains figures and tables to help interpret experiment results. 





