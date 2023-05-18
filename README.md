PROJECT STRUCTURE

DIRECTORIES
    
    DATA OBJECTS: This is where the data objects that are used to instantiate bots are kept. 

    RAW DATA: This is where all the raw data to create association lists, word lists, reduced language models, etc is found. 

    PLAY GAMES: This is where all the magic happens

        AI COMPONENTS: This file contains all of the components that are shared among various bots. The purpose of these components are
        to reduce code repetition

        CODEMASTERS: These files are the actual codemaster bot type objects that are instantiated by inputting the files they use

        GUESSERS: These files are the actual guesser bot type objects that are instantiated by inputting the files they use

        ***Note: Each guesser and codemaster bot has a different type and uses diffent underlying language model. The type specifies how the language model is used. For example, a w2v associator selects words from the w2v model differently than a w2v distance associator would, but they both use the same languge model. On the other hand, a w2v associator and a glove associator use different language model but the same bot object type to be instantuated. The only difference is that they are different instances of the same object with differing language models passed in at creation. 

        UTILS: This directory contains a lot of the objects that are manipulated throughout the experiments/touraments. It also contains utils that the different objects use. Most of thise objects are instantiated in the Object manager which is passed around files and manipulated throughout the different experiments. If there are any keys for the differing data structues, they are kept here and can be accessed through the object manager because it loads all of them up at initialization. 

            ANALYSIS FILES: This is its own directory because there is a lot to it and it helps things be more organized. The class files and utils files are mostly used by the ResultsAnalyzer object. 

                PARSERS: Contains parser objects for the different log types and adds the findings to the StatsObject

                LEARN LOG ANALYSIS: These files are used to create learn log analysis files which are the root of this project. Are most important findings are created with these files. 

    STATS: 

        SAVED RESULTS: This is where all of the saved results of learning experiments, parameter experiments, and tounaments are stored.
    
            Each tournament/learning experiment/parameter experiment is saved according to the settings in experiment settings. Each experiment is given a unique name based on what it's called in the config file and its parameters or based off of the custom name specified in experiment_settings.py. 

            Learning experiments and parameter experiments are made up of tournaments and every tournament has game logs, round logs, table logs, score logs, and cm stats. Each tournament has a unique name and so does each experiment. 

            The structure of an individual tournament is saved_results/tournaments/game_logs, round_logs, table_logs, score_logs, cm_stats, raw_data, processed_data, or visualizations/
            - There will be one of each file type for each tournament

            The structure of a learning experiment is saved_results/learning_experiments/round_logs, game_logs, table_logs, score_logs, cm_stats, learn_logs, learn_period_analyses, learn_experiment_analyses, raw_data, processed_data, or visualizations/(unique experiment name)(/) <--- I put this here in parentheses to indicate that unique experiment name is a directory for everything except for learn_experiment_analyses, raw_data, or processed_data. For that individual case, unique experiment name will be a file to uniquely identify the lean_experiment_analysis file for that experiment. 
                - There will be many of each file type for every experiment except for learn_experiment_analyses, so those will all be numbered. 

            The sturcture of a parameter experiment is the same as learning experiment with the exception that it doesn't have learn_logs, learn_period_analyses, or learn_experiment_analyses. Instead of learn_experiment_analyses, it has experiment_analyses, raw_data, processed_data, and visualizations where there isn't an individual directory for each tournament and has a single file instead. For everything else there is a directory. 

    TEST FILES: This is where all the unit tests are kept. The run_tests file imports these tests and the object manager and then passes in the needed parts of the object manager to the different tests to undergo testing. The structure of this should be the same as the structure of the entire project for everything that needs to be tested. 

PROJECT STRUCTURE RULES:

    Imports should be done from the 'play_games' level. Insert the path of the repo using the os mudule to get the cwd and the sys module to insert the 
    path to the PATH variable. 

    Put key objects in utils folders and then import those objects into a cental object manager
    to avoid unnecessary imports in other files. 
        - Any dictionaries that need to be accessed in other files should by put on the object manager. 

    All imported objects that are manipulated throughout the project should be imported only by the object manager once. 

    The object manager should only be imported at the top level of whatever program you are running and then passed in as an argument to 
    whatever files that use it. This will make it so you don't have to worry about having multiple instances of the ObjectManager class. 
    This will make it so if you change a varible on one of the objects managed by the ObjectManager in one file, you will be able to see those
    changes on the other file. This is powerful because it will allow us to gather statistics and only need to compute them once. 

    All objects with dictionaries should have the key objects instantiated in the object manager and should have the keys passed into the object. This way those keys are used within the object to build the dictionary and that same data in that dictionary can be accessed by the same keys that are passed into other objects because those same keys were passed the keys by the object manager. 

    Testing file structure should match the file structure of the repo

PROJECT STYLE

    No Enums- Use an object with strings assigned to key variables instead to avoid hard coding things. I will call these key objects

    Minimal hard coded values- use objects with key variables that contain the hard coded strings. 

    file names should be all lower-case separated by underscores. 

    file paths should be system independent. We should use the os package to concatenate and create directories/filepaths

    Objects should be camel-case with the first letter capitalized. 

    all public variables of objects must be in all caps and all private variables should be in lowercase and underscore separated

    Testing file directories should match the names of the directories in the repo but with the "_tests" suffix.
    Likewise, testing file names should match the names of the files in the repo but with the "test_" prefix.

OBJECT DISCUSSION - The objects are described in the order that they need to be instantiated. For example, if file A depends on file B, file B is described before file A. 

    ---------------------------------------------------INDEPENDENT OBJECTS------------------------------------------------------

    LM Types: This object has all of the different kinds of language models as variables with integer values

    dependencies: none

    location: play_games/utils/utils.py

    ----------------------------------------------------------------------------------------------------------------------------

    Bot Types: This object has the names for each individual bots. It's like an enum with bot name strings as the values.

    dependencies: none

    location: play_games/utils/utils.py

    ----------------------------------------------------------------------------------------------------------------------------

    AI Types: This object has all of the different AI types used in the object. It is like an enum with integers as the values for each AI type variable name

    dependencies: none

    location: play_games/utils/utils.py

    ----------------------------------------------------------------------------------------------------------------------------

    Parameters: This object has all of the different parameters that can be manipulated/set in experiment settings and used for parameter experiments depending on the bot used. 

    dependencies: none

    location: play_games/utils/utils.py

    ----------------------------------------------------------------------------------------------------------------------------

    Config Keys: These are the keys used to access data in the config file

    dependencies: none

    location: play_games/utils/utils.py

    ----------------------------------------------------------------------------------------------------------------------------

    Experiment Types: There are two variables, PARAMETER_EXPERIMENT and LEARNING EXPERIMENT

    dependencies: none

    location: play_games/utils/utils.py

    ----------------------------------------------------------------------------------------------------------------------------

    Bot Constructor Types: This object holds keys for the bot constructor types

    dependencies: none

    location: play_games/utils/utils.py

    ----------------------------------------------------------------------------------------------------------------------------

    Stats: This object as all of the different types of stats that we gather

    dependencies: none

    location: play_games/utils/analysis_files/analysis_utils.py

    ----------------------------------------------------------------------------------------------------------------------------

    Learn Parse Keys: Contains the keys needed to parse learn logs

    dependencies: none

    location: play_games/utils/analysis_files/analysis_utils.py

    ----------------------------------------------------------------------------------------------------------------------------

    Round Parse Keys: Contain the keys needed to parse round logs

    dependencies: none

    location: play_games/utils/analysis_files/analysis_utils.py 

    ----------------------------------------------------------------------------------------------------------------------------

    Min Max Keys: contain MIN and MAX constant keys

    dependencies: none

    location: play_games/utils/analysis_files/analysis_utils.py 

    ----------------------------------------------------------------------------------------------------------------------------

    Desired Stats Keys: Used to access data in Desired Stats object. Contains the Optimal Value and Extreme for each stat

    dependencies: none

    location: play_games/utils/analysis_files/analysis_utils.py 

    ----------------------------------------------------------------------------------------------------------------------------

    File Name Directory Elements: Contains the different elements needed for naming a file and building new file paths/directories. These are common constants that are used to create names. Used to instantiate file paths by File Manager at runtime. 

    dependencies: none

    location: play_games/utils/file_manager.py

    ----------------------------------------------------------------------------------------------------------------------------

    File Paths Object: This object stores all of the filepaths for the project. This will get manipulated throughout the project depending on the experiment settings and the computer file system. The paths are instantiated by the File Manager at runtime. 

    dependencies: none

    location: play_games/utils/file_manager.py

    ----------------------------------------------------------------------------------------------------------------------------

    Bot Settings Object: This object holds the parameters that are passed into a bot constructor to instantiate it. 

    dependencies: none

    location: play_games/utils/bot_settings_obj.py

    ---------------------------------------------------DEPENDENT OBJECTS--------------------------------------------------------

    Desired Stats: This object contains a dictionary that maps each stat type to a dictionary that contains the optimal value and extreme (min or max) for a stat. This data can be accessed using the Desired Stats Keys. 

    dependencies: Stats, Min Max Keys, and Desired Stats Keys

    location: play_games/utils/analysis_files/analysis_utils.py 

    ----------------------------------------------------------------------------------------------------------------------------

    Bot Paths: This object maps each Bot Type to the files that it needs to get instantiated

    dependencies: Bot Types and File Paths Object

    location: play_games/utils/bot_parameter_settings.py

    ----------------------------------------------------------------------------------------------------------------------------

    Bot AI Types: This is an object that maps each bot type Bot Type to an AI type

    dependencies: AI Types and Bot Types

    location: play_games/utils/bot_parameter_settings.py

    ----------------------------------------------------------------------------------------------------------------------------

    Bot LM Types: This is an object that maps each bot type Bot Type to an LM type

    dependencies: AI Types and LM Types
    
    location: play_games/utils/bot_parameter_settings.py

    ----------------------------------------------------------------------------------------------------------------------------

    Experiment Settings: To hold all the settings for experiments and tournaments
    - It is also used to query information about the settings 

    dependencies: (passed in from Object Manager)
    - AITypes
    - BotAITypes
    - ExperimentTypes

    location: play_games/utils/experiment_settings.py

    ----------------------------------------------------------------------------------------------------------------------------

    Round Log Parser: parses round logs and creates a raw data dictionary that is saved

    dependencies: RoundParseKeys, Stats, and FileManager

    location: play_games/utils/parsers/round_log_parser.py

    ----------------------------------------------------------------------------------------------------------------------------

    Learn Log Parser: parses learn logs and creates a raw data dictionary that is saved

    dependencies: LearnParseKeys, Stats, and FileManager

    location: play_games/utils/parsers/learn_log_parser.py

    -------------------------------------------Double-Dependent Objects----------------------------------------------------------

    File Manager: a tool for managing file objects. 
    - It uses file nameing fragments that are used to create unique filenames for logging/result files based off of experiment settings. 
    - It creates directories and files in the OS for the current tournaments and experiments specified in experiment settings. 
        - It saves the new filepaths in the File Paths Obj
    - It manages open files
    - It interacts with File Paths Object and File Name Elements object to change the names of the filepaths depending on the experiment settings
    - It creates, moves, and deletes files in the system

    dependencies: 
    - ExperimentSettings
    - AITypes
    - FilePathsObj
    - BotAITypes
    - ExperimentTypes
    - FileNamDirectoryElements 

    location: play_games/utils/file_manager.py

    ----------------------------------------------------------------------------------------------------------------------------

    Results Analyzer: This is the file that analyzes all of the results. It parses the logs, saves the data after parsing by using file paths built by FileManager using FileNameDirectoryElements saved in FilePathsObj. I then uses the dictionary returned by the parsers and analyzes them to build another dictionary with calculated stats. It saves that dictionary and then uses it to build tables and other visualizations

    dependencies: 
    - ExperimentSettings
    - RoundLogParser
    - LearnLogParser
    - Stats
    - StatDictKeys
    - FileManager

    location: play_games/utils/results_analyzer.py 

    ----------------------------------------------------------------------------------------------------------------------------

    Bot Initializer: This object initializes the bots needed for a given set of games in a pairing in a tournament. 

    dependencies: 
    - AITypes
    - BotAITypes
    - BotPaths
    - BotTypes
    - BotConstructorTypes

    location: play_games/utils/bot_initializer.py

    ----------------------------------------------------------------------------------------------------------------------------

    Bot Objects: This object is passed in a dictionary of bot constructors that the object manager creates and passes in. The keys of this dictionary are Bot Constructor Types
    and the keys are the actual Bot Constructors. The purpose of this is so that we don't need to continually import constructors in multiple places. If a constructor is needed, the Constructor Type key is passed in and a copy of the Bot is returned. This is double-dependent because it indirectly depends on the actual bot constructors, which depend on other files. 

    dependencies: Bot Constructor Types and all of the constructors (both indirectly)

    location: play_games/utils/bot_objects.py


    ----------------------------------------------------------------------------------------------------------------------------

    The Actual Bots: These objects are the actual Codemasters or Guessers. They don't have normal constructors because we want to be able to initialize them in the Object Manager and make clean copies when we query the bots from Bot Objects. Instead, we have a sort of pseudo-constructor called initialize which will take all the information specific for that bot and acutally initialize the data needed for that bot to perform as wanted. 

    dependencies: AI Components and other raw data files

    location: play_games/codemasters or guessers/Bot Constructor Type name

    ----------------------------------------------------------------------------------------------------------------------------

    Object Manager: a tool for managing object interactions. Imports all the objects in one centralized location so that if things are changed, the changes persist throughout the entire game and so we don't have so many pieces being passed around. It also simplifies imports. 

    dependencies: almost all other objects

    location: /play_games/utils/object_manager.py


TESTING

The testing will be centralized in the run_tests file. 

Run Tests: This file utilizes the Test Keys and puts them in an array. Run tests iterates through this list and passes each one to Testing File Manager which will run the test and output the results 

Testing File Manager: This file imports all of the test files and can run them individually. Every test has a function called test() which is called. When this is called, Object Manager is passed in which contains everything that the test might need to test a specific functionality. 

Testing Utils: This file contains the keys to the individual tests. Run Tests imports this and passes it into Testing File Manager in the constructor. These keys are then used to query specific tests. 

