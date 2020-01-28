'''
A sample code usage of the python package stanfordcorenlp to access a Stanford CoreNLP server.
Written as part of the blog post: https://www.khalidalnajjar.com/how-to-setup-and-use-stanford-corenlp-server-with-python/

https://www.khalidalnajjar.com/setup-use-stanford-corenlp-server-python/
'''

from stanfordcorenlp import StanfordCoreNLP
import time

# PLATFORM CONFIG
coreNLPdir = '/home/john/Applications/stanford-corenlp-full-2018-10-05'
host = 'http://localhost'
port = 9000
timeout = 30000

# NLP SETTINGS
props = {
            'annotators': 'tokenize, cleanxml, ssplit, pos, lemma, ner, parse, depparse, dcoref',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }

# TEST INPUT
# text = "A blog post using Stanford CoreNLP Server. Visit www.khalidalnajjar.com for more details."
text = "David Crandall is working on AI and Vision. He lives in Bloomington."



if __name__ == '__main__':
    nlp = StanfordCoreNLP(host, port=port, timeout=timeout)
    # nlp = StanfordCoreNLP(coreNLPdir)
    t0 = time.perf_counter()
    res = nlp.annotate(text, properties=props)
    print(time.perf_counter()-t0)
    ofp = open('res.json', mode='w', encoding='utf8')
    ofp.write(res)
    ofp.close()





