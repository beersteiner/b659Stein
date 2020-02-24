from slugify import slugify
from urllib.request import urlretrieve
from urllib.parse import urlparse
from bs4 import BeautifulSoup

srcs = [
    "https://medlineplus.gov/ency/article/002458.htm",
    ""
]

for src in srcs:
    fn = "dataRaw_" + slugify(src)
    urlretrieve(src, filename=fn)
    with open(fn) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

        print(soup.prettify())

        fp.close()