"""Retrieves and summarizes titles from Nikkei Keizai Shimbun."""

from urllib.request import urlopen
from bs4 import BeautifulSoup as BS

def get_titles(soup):
    """Return text from article titles, with ideographic space stripped."""
    titles = soup.select('span[class*="k-card__title-piece"]')
    title_text = [t.text.strip().replace('\u3000','') for t in titles]
    return title_text

def main():
    """Retrieve and summarize titles from Nikkei Keizai Shimbun."""
    url = urlopen("https://www.nikkei.com/")
    soup = BS(url, 'html.parser')
    title_text = get_titles(soup)
    print(title_text)

if __name__ == "__main__":
    main()
