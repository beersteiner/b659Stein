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
    return True


# Recursively extract text from an element tree
def elementDFS(e, t):
    for c in e.children:
        if c.string:
            t += str(c.string)                          # accumulate text
            if type(c) != type(e): t += "\n"            # if leaf/navigable-string
        elif type(c) == type(e):                        # this element is a tag
            if qualifyChild(c): t = elementDFS(c, t)    # recur through children
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



# Hard-coded (for now) example urls to search
srcs = [
    "https://medlineplus.gov/ency/article/002458.htm",
    "https://www.healthline.com/nutrition/11-most-nutrient-dense-foods-on-the-planet",
    "https://www.healthline.com/nutrition/50-super-healthy-foods",
    "https://www.bbc.com/future/article/20180126-the-100-most-nutritious-foods",
    "https://familydoctor.org/changing-your-diet-choosing-nutrient-rich-foods/",
    "https://www.webmd.com/vitamins-and-supplements/features/healthy-foods#1",
    "https://www.choosemyplate.gov/eathealthy/protein-foods/protein-foods-nutrients-health",
    "https://www.health.harvard.edu/staying-healthy/add-more-nutrient-dense-foods-to-your-diet",
    "https://www.foxnews.com/health/foods-that-work-better-together",
    "https://www.health.com/nutrition/11-superfoods-that-work-better-together",
]

# Iterate through urls
for src in srcs:
    snm = slugify(src) # establish base file stem name

    # Retrieve and save source html file
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

        # create soup object and extract text
        with open("dataClean_" + snm + ".txt", mode='wt') as outfile:
            out1 = elementDFS(soup.find(), "")  # grab first root element and extract text via DFS
            out2 = clean(out1)                  # clean/process text
            outfile.write(out2)                 # save to file
            outfile.close()