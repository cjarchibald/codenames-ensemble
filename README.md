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


