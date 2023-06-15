The files in this folder were used to train the CoLT model. 

There are three jupyter notebook files. 

1. generate_colt_model_training_data

This file generates random team feature vectors, then simulates a game between them, then creates data points with the difference of vectors and the estimated win percentage from the simulations.  The data files are saved in the 'data' folder

2. train_and_save_colt_model

This file will load the data and train a pytorch colt model. After training it will show the model R2 score on a holdout test set and then save the model to the 'data' folder

3. convert_colt_model_torch_to_skl

This file will load the trained pytorch colt model and convert it to an equivalent sklearn colt model.  This was the format that was easier to use within the rest of our codebase. 