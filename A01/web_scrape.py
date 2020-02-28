from slugify import slugify
import urllib.request, shutil
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import nltk, re


# Only explore child elements that pass these tests
def qualifyChild(e):
    if e.name in [
        "head",
        "script",
        "noscript",
    ]: return False     # don't expect natural language to reside in head or scripts
    return True

# Only accept text from elements that pass these tests
def qualifyElement(e):
    if e.name in [
        "button",
        "a",
    ]: return False                                     # ignore buttons and links/anchors
    if type(e.text) != str: return False                # make sure text is unicode/str
    if len(e.text) < 1: return False                    # ignore empty strings
    return True

# Recursively extract text from an element tree
def recursiveText(e, t):
    children = e.findChildren(recursive=False)          # get child elements
    if len(children) > 0:                               # DFS through tree
        for c in children:
            if qualifyChild(c): t = recursiveText(c, t) # recur through children
    elif qualifyElement(e):                             # if leaf, get text
        t = t + e.get_text() + "\n"                     # accumulate text
    return t

# Clean and process resulting text
def clean(t):
    assert (type(t) == str)                     # ensure unicode
    res = ""
    t = re.sub('\n\n+', '\n', t)                # remove repeating \n chars
    pars = t.split("\n")                        # process paragraph
    for p in pars:
        sents = nltk.sent_tokenize(p)           # find sentence boundaries
        res = res + "\n".join(sents) + "\n\n"   # add extra \n at end of paragraph
    return res




srcs = [
    "https://medlineplus.gov/ency/article/002458.htm",
    "https://www.healthline.com/nutrition/11-most-nutrient-dense-foods-on-the-planet",
    "https://www.healthline.com/nutrition/50-super-healthy-foods",
    "https://www.bbc.com/future/article/20180126-the-100-most-nutritious-foods",
    "https://familydoctor.org/changing-your-diet-choosing-nutrient-rich-foods/",
]

for src in srcs:
    snm = slugify(src) # establish base file stem name

    # Retrieve and save source html file
    # urlretrieve(src, filename="dataRaw_" + snm)
    req = urllib.request.Request(
        src,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) \
                Gecko/20100101 Firefox/72.0'  # needed for https requests
        }
    )
    with urllib.request.urlopen(req) as response, open("dataRaw_" + snm, 'wb') as htmlfile:
        shutil.copyfileobj(response, htmlfile)

    # Scrape text from saved html file
    with open("dataRaw_" + snm, mode='r') as htmlfile:
        soup = BeautifulSoup(htmlfile, 'html.parser')

        # Get title, author, url and save to "meta_" + fn
        with open("dataMeta_" + snm + ".txt", mode='wt') as metafile:
            meta = ""
            res = soup.find(name='title')
            if res: meta = res.text + '\n'
            res = soup.find(name='author')
            if res: meta = res.text + '\n'
            meta = meta + src
            metafile.write(meta)
            metafile.close()

        # Obtain result set and extract text
        with open("dataClean_" + snm + ".txt", mode='wt') as outfile:
            out1 = recursiveText(soup.find(), "")
            out2 = clean(out1)
            outfile.write(out2)
            outfile.close()