"""Retrieves and summarizes titles from Nikkei Keizai Shimbun."""

from kanjidictionary import KanjiDictionary
from urllib.request import urlretrieve, urlopen
from collections import Counter
from datetime import date
import re
import os
import argparse
import heapq as hq
from lxml import etree
from bs4 import BeautifulSoup as BS
import pandas as pd

TERMINAL_WIDTH = os.get_terminal_size().columns
SCRAPE_DIR = 'data'
SUMMARY_DIR = 'summary'
TODAY = date.today().strftime("%Y%m%d")

def get_title_elements(soup):
    """Get title elements from the homepage"""
    title_elements = soup.select('article')
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

def get_nikkei225():
    """Return Nikkei index."""
    soup = BS(urlopen("https://www.nikkei.com/markets/worldidx/chart/nk225/"), 'html.parser')
    nikkei225 = soup.select_one('span[class^="economic_value_now"]').text
    return nikkei225

def extract_kanji(text):
    """Extract only kanji from the title."""
    regex = re.compile(u'[^\u4E00-\u9FFF]+') #CJK Unified Ideographs (kanji unicode)
    return regex.sub('', text)

def print_titles(titles, num, nikkei225):
    """Prints top n titles"""
    print("NIKKEI 225: {}".format(nikkei225).center(TERMINAL_WIDTH, "="))
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
        barwidth = '█' * bar_chunks
        if remainder > 0:
            barwidth += chr(ord('█') + (8 - remainder))
        barwidth = barwidth or '▏'
        print(f'{kanji.rjust(1)} ▏ {count:#4d} {barwidth}')

def get_kanji_info(kanji, kanji_dic):
    """Returns grade (str) and stroke count (int) for kanji through lookup in kanji_dic"""
    try:
        grade = kanji_dic[kanji]['grade']
        stroke_count = kanji_dic[kanji]['stroke_count']
        stroke_count = int(stroke_count) if stroke_count.isdigit() else None 
        return grade, stroke_count
    except KeyError:
        return None, None

def retrieve_today_scrape(scrape_suffix):
    """Retrieves filepath of today's scrape from data folder if exists, otherwise creates it"""
    filepath = os.path.join(SCRAPE_DIR, TODAY + scrape_suffix)
    if not os.path.exists(SCRAPE_DIR):
        os.makedirs(SCRAPE_DIR)
    if not os.path.isfile(filepath):
        urlretrieve("https://www.nikkei.com/", filepath)
    return filepath

def append_summary_to_file(kanjicnt, filename):
    """Append the contents of the Counter kanjicnt to the csv 'filename'"""
    today_df = pd.DataFrame.from_dict(kanjicnt, orient='index')
    today_df.columns = [TODAY]

    filepath = os.path.join(SUMMARY_DIR, filename)
    if not os.path.exists(SUMMARY_DIR):
        os.makedirs(SUMMARY_DIR)
    if not os.path.isfile(filepath):
        today_df.to_csv(filepath, index = True)
    elif os.path.isfile(filepath):
        existing_df = pd.read_csv(filepath, index_col = 0)
        if TODAY in existing_df.columns:
            pass
        else:
            new_df = existing_df.join(today_df, how='outer')
            new_df.to_csv(filepath, index = True)

def get_difficulties(kanji_cnt, kanji_tree, grade_weight = 1):
    """Return a dictionary of difficulties (kanji keys, weighted difficulty values)"""
    difficulties = {}
    for kanji in kanji_cnt:
        grade, stroke_count = get_kanji_info(kanji, kanji_tree)
        if None not in (grade, stroke_count):
            difficulties[kanji] = grade_weight*int(grade) + (1-grade_weight)*int(stroke_count)
        else:
            pass
    return difficulties

def display_difficulties(difficulties, num):
    """Prints top n difficulties and mean difficulty"""
    print("Highest difficulty kanji: Top {} of {}".format(num, len(difficulties)).center(TERMINAL_WIDTH, "_"))
    hardest = hq.nlargest(num, difficulties, key=difficulties.get)
    print(*zip(hardest, [difficulties.get(h) for h in hardest]), sep='\n')

def main():
    """Retrieve and summarize titles from Nikkei Keizai Shimbun."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--d", dest='display',
                        action='store_true',
                        default = False,
                        help="Display latest headlines and kanji")
    parser.add_argument("--w", dest='grade_weight',
                        action='store',
                        default = 1.0,
                        type = float,
                        help="Number between 0.0 and 1.0 indicating grade weight")
    args = parser.parse_args()

    scrape = retrieve_today_scrape('nikkei.html')
    soup = BS(open(scrape), 'html.parser')
    title_elements = get_title_elements(soup)
    titles, kanji_cnt  = parse_titles(title_elements)
    nikkei225 = get_nikkei225()
    append_summary_to_file(kanji_cnt, "summary.csv")

    kanji_dic = KanjiDictionary('inputs/kanjidic2.json').get_dict()
    difficulties = get_difficulties(kanji_cnt, kanji_dic,
                                    grade_weight = args.grade_weight)

    if args.display:
        print_titles(titles, 5, nikkei225)
        display_top_kanji(kanji_cnt, 15)
        display_difficulties(difficulties, 10)

if __name__ == "__main__":
    main()
