"""Retrieves and summarizes titles from Nikkei Keizai Shimbun."""

from urllib.request import urlretrieve
from os.path import isfile
from os import get_terminal_size
from collections import Counter
import re
from lxml import etree
from bs4 import BeautifulSoup as BS

TERMINAL_WIDTH = get_terminal_size().columns

def get_title_elements(soup):
    """Get title elements from the homepage"""
    title_elements = soup.select('span[class*="k-card__title-piece"]')
    return title_elements

def parse_titles(title_elements):
    """Get list of titles (text) and Counter of kanji (across all titles)"""
    titles = [None] * len(title_elements)
    kanji_cnt = Counter()
    for idx, title in enumerate(title_elements):
        clean_title = title.text.strip().replace('\u3000', '') #strip ideographic space
        titles[idx] = clean_title
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

def print_titles(titles, num):
    """Prints top n titles"""
    print("Headlines: Top {} of {}".format(num, len(titles)).center(TERMINAL_WIDTH, "_"))
    print(*titles[:num], sep='\n')

def display_top_kanji(kanji_cnt, num):
    """Displays bar chart of top n kanji"""
    print("Kanji: Top {} of {}".format(num, len(kanji_cnt)).center(TERMINAL_WIDTH, "_"))
    max_value = kanji_cnt.most_common(1)[0][1]
    increment = max_value/25
    for kanji, count in kanji_cnt.most_common(num):
        #ASCII bar chart from https://alexwlchan.net/2018/05/ascii-bar-charts/
        bar_chunks, remainder = divmod(int(count * 8/increment), 8)
        bar = '█' * bar_chunks
        if remainder > 0:
            bar += chr(ord('█') + (8 - remainder))
        bar = bar or '▏'
        
        print(f'{kanji.rjust(1)} ▏ {count:#4d} {bar}')

def get_stroke_count(kanji_element):
    try: 
        return kanji_element.findtext("misc/stroke_count")
    except (IndexError, AttributeError):
        return None

def get_grade(kanji_element):
    try:
        return kanji_element.findtext("misc/grade")
    except (IndexError, AttributeError):
        return None
    

def get_kanji_info(kanji, kanji_tree):
    kanji_element = kanji_tree.xpath("//character[literal = '%s']" % kanji)[0]
    grade = get_grade(kanji_element)
    stroke_count = get_stroke_count(kanji_element)
    return grade, stroke_count

def main():
    """Retrieve and summarize titles from Nikkei Keizai Shimbun."""
    if not isfile('nikkei.html'):
        urlretrieve("https://www.nikkei.com/", "nikkei.html")
    if not isfile('kanjidic2.xml'):
        raise FileNotFoundError('File kanjidic2.xml not found in local directory. Install from the KANJIDIC Project at edrdg.org')

    soup = BS(open('nikkei.html'), 'html.parser')
    title_elements = get_title_elements(soup)
    titles, kanji_cnt  = parse_titles(title_elements)
    nikkei225 = get_nikkei225(soup)
    
    kanji_tree = etree.parse('kanjidic2.xml')
    character = '試'
    grade, stroke_count = get_kanji_info(character, kanji_tree)

    print_titles(titles, 5)
    display_top_kanji(kanji_cnt, 15)

if __name__ == "__main__":
    main()
