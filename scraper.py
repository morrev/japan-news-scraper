"""Retrieves and summarizes titles from Nikkei Keizai Shimbun."""

from urllib.request import urlretrieve
from os.path import isfile
from bs4 import BeautifulSoup as BS

def get_titles(soup):
    """Return text from article titles, with ideographic space stripped."""
    titles = soup.select('span[class*="k-card__title-piece"]')
    title_text = [t.text.strip().replace('\u3000','') for t in titles]
    return title_text

def get_nikkei225(soup):
    """Return Nikkei index."""
    nikkei225 = soup.select_one('span[class*="k-hub-market__current-price"]').text
    return nikkei225

def main():
    """Retrieve and summarize titles from Nikkei Keizai Shimbun."""
    
    if not isfile('nikkei.html'):
        urlretrieve("https://www.nikkei.com/", "nikkei.html")
    soup = BS(open('nikkei.html'), 'html.parser')
    
    title_text = get_titles(soup)
    nikkei225 = get_nikkei225(soup)
    print(title_text)
    print(nikkei225)

if __name__ == "__main__":
    main()
