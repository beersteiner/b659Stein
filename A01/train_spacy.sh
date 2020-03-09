#!/bin/bash

# Train models from .train.json and .dev.json files in data/
# User specifies number of training cycles

datadir='data/'

if [ $# -eq 0 ]
then
	echo "Please supply number of training cycles as argument";
fi

# command to train spacy models on the split all.conll data
# user must specify number of training cycles
python -m spacy train en spacymodel "${datadir}"all.train.json "${datadir}"all.dev.json -n $1;




