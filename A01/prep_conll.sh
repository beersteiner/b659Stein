#!/bin/bash

# directory where data resides
datadir='data/'

# initialize the empty consolidated file
echo "" > "${datadir}"all.conll;

# append all conll files into all.conll
for f in `ls "${datadir}"*.conll | egrep -v -e '\.(dev|test|train)\.conll' -e 'all\.conll'`
do
	#echo "adding ${f}";
	cat "${f}" >> "${datadir}"all.conll;
done

# split all.conll into test, dev, and training
python generateTrainingDevTest.py "${datadir}"all.conll;

# Convert test, dev, and training files into json
for f in `ls "${datadir}" | egrep -v '.*\.json' | egrep -o 'all\.(dev|test|train)'`
do
        #echo "${f}.conll"
        python -m spacy convert -l en -t json -c ner "${datadir}${f}".conll > "${datadir}${f}".json;
done
