"""Retrieves and summarizes titles from Nikkei Keizai Shimbun."""

from urllib.request import urlretrieve
from os.path import isfile
from collections import Counter
import re
from bs4 import BeautifulSoup as BS

def get_title_elements(soup):
    """Get title elements from the homepage"""
    title_elements = soup.select('span[class*="k-card__title-piece"]')
    return title_elements

def parse_titles(title_elements):
    """Get list of titles (text) and Counter of kanji (across all titles)"""
    titles = set()
    kanji_cnt = Counter()
    for title in title_elements:
        clean_title = title.text.strip().replace('\u3000', '') #strip ideographic space
        titles.add(clean_title)
        kanji_cnt += Counter(extract_kanji(clean_title))
    return titles, kanji_cnt

def get_nikkei225(soup):
    """Return Nikkei index."""
    nikkei225 = soup.select_one('span[class*="k-hub-market__current-price"]').text
    return nikkei225

def extract_kanji(text):
    """Extract only kanji from the title."""
    regex = re.compile(u'[^\u4E00-\u9FFF]+') #CJK Unified Ideographs (kanji unicode)
    return regex.sub('', text)

def main():
    """Retrieve and summarize titles from Nikkei Keizai Shimbun."""
    if not isfile('nikkei.html'):
        urlretrieve("https://www.nikkei.com/", "nikkei.html")
    soup = BS(open('nikkei.html'), 'html.parser')
    title_elements = get_title_elements(soup)
    titles, kanji_cnt  = parse_titles(title_elements)
    nikkei225 = get_nikkei225(soup)
    print(kanji_cnt)
    print(nikkei225)

if __name__ == "__main__":
    main()
