#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Split a CoNLL file into three sub-files: training, dev, test

(C) 2019-2020 by Damir Cavar <damir@cavar.me>

Use the command line:

    python3 generateTrainingDevTest.py myfile.conll

"""


import sys
import glob
import codecs
import os.path


def main(filename):
    linecounter = []
    ifp = codecs.open(filename, encoding='utf8', mode='r')
    lines = ifp.readlines()
    ifp.close()
    pos = 0
    for l in range(len(lines)):
        if lines[l].strip():
            continue
        pos += 1
        linecounter.append(l)
    train     = round(len(linecounter) * .8)
    trainend  = linecounter[train]
    dev       = round(len(linecounter) * .9)
    devstart  = trainend + 1
    devend    = linecounter[dev]
    teststart = devend + 1

    fn = os.path.splitext(filename)
    if fn[1] in (".conll", ".txt"):
        filename = fn[0]

    ofp = codecs.open(".".join( (filename, "test", "conll") ), encoding='utf8', mode='w')
    for i in range(teststart, len(lines)):
        ofp.write(lines[i])
    ofp.close()
    ofp = codecs.open(".".join( (filename, "dev", "conll") ), encoding='utf8', mode='w')
    for i in range(devstart, devend):
        ofp.write(lines[i])
    ofp.close()
    ofp = codecs.open(".".join( (filename, "train", "conll") ), encoding='utf8', mode='w')
    for i in range(trainend):
        ofp.write(lines[i])
    ofp.close()


if __name__=="__main__":
    for x in sys.argv[1:]:
        for y in glob.glob(x):
            main(y)
