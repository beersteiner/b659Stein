#!/usr/bin/env python3


"""
Train_Model_1

Train an NER model from some CoNLL corpus

(C) 2019-2020 by Damir Cavar <dcavar@iu.edu>
"""


from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, CharacterEmbeddings, FlairEmbeddings
from typing import List
from flair.visual.training_curves import Plotter
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer



# loop over 10 different corpus selections...
for n in range(1): # just take 0

    # corpusfile = "".join( ("Result", str(n), ".conll") )
    corpusfile = "all"
    #corpusfile = "dataHandCleaned_https-familydoctor-org-changing-your-diet-choosing-nutrient-rich-foods" #, str(n), ".conll") )

    # define columns
    columns = {0: 'text', 1: 'pos', 2: 'something', 3: 'ner'}

    # this is the folder in which train, test and dev files reside
    data_folder = 'data/'

    # init a corpus using column format, data folder and the names of the train, dev and test files
    corpus: Corpus = ColumnCorpus(data_folder, columns,
                                  train_file=".".join( (corpusfile, 'train.conll') ),
                                  test_file=".".join( (corpusfile, 'test.conll') ),
                                  dev_file=".".join( (corpusfile, 'dev.conll') ) )

    # what tag do we want to predict?
    tag_type = 'ner'

    # make the tag dictionary from the corpus
    tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
    print(tag_dictionary.idx2item)

    # initialize embeddings
    # reference: https://github.com/flairNLP/flair/blob/master/resources/docs/TUTORIAL_4_ELMO_BERT_FLAIR_EMBEDDING.md
    embedding_types: List[TokenEmbeddings] = [
        WordEmbeddings('glove'),
        WordEmbeddings('extvec'),

        # comment in this line to use character embeddings
        # CharacterEmbeddings(),

        # comment in these lines to use flair embeddings
        # FlairEmbeddings('news-forward'),
        # FlairEmbeddings('news-backward'),
    ]

    embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

    # initialize sequence tagger
    tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                            embeddings=embeddings,
                                            tag_dictionary=tag_dictionary,
                                            tag_type=tag_type,
                                            use_crf=True)

    # initialize trainer
    trainer: ModelTrainer = ModelTrainer(tagger, corpus)

    # start training
    trainer.train("".join( ('flairmodel', str(n), '/taggers/example-ner' ) ),
                  learning_rate=0.1,
                  mini_batch_size=32,
                  max_epochs=150)

    # plot weight traces (optional)
    plotter = Plotter()
    plotter.plot_weights("".join( ( 'flairmodel', str(n), '/taggers/example-ner/weights.txt' ) ))
