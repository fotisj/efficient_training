# efficient_training
code for the paper efficient training for historical texts


After cloning the repository change into the subdirectory scripts. There you can 

- run the NER script from Huggingface on the commandline:

    >python run_ner.py config-bert.json

The Bert configuration should run out of the box (and the distilbert vanilla) because the pretrained model is downloaded. The others have to be installed by hand.

- run the crossvalidation script, you have to modify crossval.json to your wishes. The most important aspect is the model, you want to train. 
Then just run:

> python crossvalidation.py crossval.json


# models

## electra-small

Trained from scratch
* Data: 8GB raw text, 19.200.200 training examples (DOC-SENTENCE style, see Roberta Paper)
* Batch size: 64
* Device: RTX 2080ti 
* Training steps: 1.600.000
* Training time: 14d


