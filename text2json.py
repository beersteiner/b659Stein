#!/usr/bin/env python

"""
Author: John Stein
Description: receives text and returns json object of processed text using Damir's API & backend
"""

# IMPORTS
import sys
import argparse
import urllib
import json


# GLOBALS
server ='https://jnlp.semantic-tech.com/'           # name of Damir's RESTful service
with open('semantic-tech_creds.text', 'r') as f:    # username and password kept in non-repo file
    username = f.readline().strip()
    password = f.readline().strip()
    f.close()


# FUNCTIONS
def credentials(url, username, password):
    p = urllib.request.HTTPPasswordMgrWithDefaultRealm()    # creates password mgr object
    p.add_password(None, url, username, password)           # adds credentials
    handler = urllib.request.HTTPBasicAuthHandler(p)        # knows how to use p to authenticate to server
    opener = urllib.request.build_opener(handler)           # build an OpenerDirector instance
    urllib.request.install_opener(opener)                   # install the opener so we can use urlopen()

def text2json(s):
    url = server + '?text=' + urllib.parse.quote(s)         # construct url with url-encoded input text
    credentials(server, username, password)                 # build and install an authenticated opener
    req = urllib.request.Request(url=url)                   # create a request and open the url
    resp = urllib.request.urlopen(req).read()
    j = json.loads(resp.decode('utf-8'))                    # convert to json object
    return j

def main():
    # When this file is run
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input_text', help="Input Text", type=str)
    #parser.add_argument('-o', help="Output File", default=sys.stdout, type=argparse.FileType('w'))
    args = parser.parse_args()
    print(text2json(args.input_text))
    return 0


# RUN
if __name__ == "__main__":
    sys.exit(main())

