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


## Running Experiments

Experiments are configured in the 'config.ini' file found in 'play_games/utils'

### Learning Experiments 

A learning experiment is where we analyze how an ensemble or ACE bot learns over a fixed number of games. 'x' number of learning periods are run each comprised of 'y' number of games. 

To run one, make sure your current directory in the command line is the repository root 'codenames-ensemble'. Then run the file and specify the experiment key that you used to configure the experiment settings in 'config.ini' along with the iteration range of learning periods for your experiment. For expample, 

``` 
python play_games/file_runner.py [SPECIFY EXPERIMENT KEY HERE] [START LP] [END LP]
```

the end LP is not inclusive. 

For example, one of the commands to run the experiments we did is 

```
python play_games/file_runner.py DIST_ENS_WO 2000 3512
```

If you look in config.ini, you will see a key called DIST_ENS_WO and all of the settings associated with it. You will also see a property called 'iteration_range'. The two numbers that are part of the command above replace this property. The learning period is used to calculate a random seed for each game. 

If you run the python file without any arguments it will use the config key specified in file_runner.py and use all the settings that are already in the config.ini file without overriding any of them. 

### Parameter Experiments 

The config settings work the same way as in the learning experiments. You can do the exact same command, but instead of giving a config key associated with a learning experiment, you give one associated with a parameter experiment. This runs 'x' number of games for every sequenctial value 'y' in iteration range for every independent variable specified under the config key in config.ini. 

*NOTE: The only independent variable available to tweak at the moment is 'n_associations' and 'ensemble_parameters'. However, you can add another property to the file and make sure that its value is a list that can either have length one or more. If the list is longer than one, it will be considered the independent variable that is being tested. 

## File Naming 

The root file name can be specified in the config file with the settings for your experiment under the 'custom_root_name' property. If this is set to none, a default name, unique to the experiment settings, is generated. This unique name is usually comprised of the settings specific to the type of experiment you are running. 

If you see more files with different non-minor differences in the same directory (differ by more than just a single number near the ind of the filename), then they are from a different experiment. 

Because file names are unique to the experiment settings, but not to when they are run, if you run the same experiment twice, the old files will be replaced with the new ones. 

## Saved Experiment Data 

In the stats/saved_results directory and both the learning and parameter experiments, you will find sub-directories called 'raw_data', 'parsed_data', 'processed_data', 'raw_data', and 'visualizations'. These are the sequential steps in the data processing/prep pipeline for the project. 'raw_data' contains all of the round and learn logs. These are the files that are written to during an experiment. 'parsed_data' has all of the data parsed from each learning period's learn logs and round logs. 'processed_data' has all of transformed data for every learning period in the experiment alond with a sumarizing file that averages the data accross all learning periods for each stat. 'visualizations' contains tables and figures that show the data contained in 'processed_data'. You can indicate which files belong to which experiment by the file names. 

## Experiment Visualizations 

When an experiment is run, different experiments are generated as a result. The names of these figures can be found in their corresponding directories by the unique name generated for the specific experiment. 

### Learning Experiments

Under the sub-directory 'stats/saved_results/learning_experiments/visualizations , you will see two sub-directories: 'figures' and 'tables'. Under tables, you will see another directory called 'learn_tables'. Here, you will find tables that display summarizing stats for bot pairings across all learning periods. Because this is a learning experiment, this means that there is a bot that learns. That bot is compared against the baseline distance associator bots in the top left corner of the table. 

Under the 'figures/learn_figs' sub-directory, you will find more sub-directories for different kinds of visualizations. 
- The 'arm_weights_figs' show the weights assigned to each arm in an ACE bot with it's teammates averaged over all the learning periods. 
- The 'percent_selected_figs' show the percentage of the time that all of the arms are selected in an ACE bot averaged across all learning periods. 
- The 'performance_progression_figs' contains sub-directories for each main statistic that shows how the running average averaged across all learning periods for each game changes for each main statistic across the 'n' games in each learning period. 
- The 'performance_progression_sliding_window_figs' contains sub-directories for each main statistic that shows how the average from the current game until the last game changes across all games in a learning period. The numbers in the plot are attained by averaging across all learning periods for each corresponding game number. 

### Parameter Experiments

Because this wasn't the main focus of our research, we don't have nearly as many visualizations. 

Under the sub-directory 'stats/saved_results/parameter_experiments/visualizations/figures/param_comparison_figs' you can find figures that compare the average score for each stat accross all games played 

## Main Statistics 

The main statistics that we kept track of were: 
- Win Rate: Percentage of time a team wins
- Average Win Time: The average number of turns it takes for a team to win when it wins. 
- Minimum Win Time: The fewest nummber of turns it took a team to win. In the case of a learning period, when looking at the tables you will see that this isn't an integer. This is because this uses the average minumum win time across all learning periods. 
- CoLT Score: In the case of a learning experiment, this is the average CoLT score accross all learning periods. 
- Average Red Words Flipped Per Game: red words are the words belonging to the bot team playing. Higher is better. 
- Average Blue Words Flipped Per Game: blue words are the words belonging to the other team. Lower is better. 
- Average Bystander Words Flipped Per Game: bystander words are the words that don't belong to either team. Lower is usually better. However, this depends on the strategy used by the bot team. 
- Average Assassin Words Flipped Per Game: This is always a number between 1 and 0 because there is at most 1 assassin flipped per game. Lower is always better. 







