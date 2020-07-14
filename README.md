# efficient_training
code for the paper efficient training for historical texts


After cloning the repository you can 

- run the NER script from Huggingface on the commandline:

    >python run_ner.py config-bert.json

The Bert configuration should run out of the box (and the distilbert vanilla) because the pretrained model is downloaded. The others have to be installed by hand.

To run the crossvalidation script, you have to modify crossval.json to your wishes and you have to make sure that the information in crossval.json is the same as in the configuration file you are pointing it to.
Then just run:

> python crossvalidation.py crossval.json


