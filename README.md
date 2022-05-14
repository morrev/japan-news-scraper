japan-news-scraper
==========

Simple study aid to display daily headlines, most frequent kanji, and highest difficulty kanji (based on grade level and stroke count).
The difficulty is defined as: `(grade_weight)*(grade level) + (1 - grade_weight)*(stroke count)`
By default the grade_weight is set to 1 (i.e. by default, do not consider stroke count).

Running
----
Running scraper.py without arguments appends the latest kanji frequencies (extracted from the Nikkei 225 homepage) to summary/summary.csv:  
``` python
python scraper.py
```
Arguments:
- `--d` displays the scraping output (otherwise, silently scrapes and appends to csv)
- `--w 0.5` sets the grade weight to 0.5

For example, to display top kanji on the Nikkei homepage by difficulty, with equal weights for kanji grade level and stroke count:
``` python
python scraper.py --d --w 0.5
```

Current functionality
----
![Example](/images/example2.png)

Setup/Dependencies
----
Requires "kanjidic2.xml" (data on kanji grade level and stroke count) at the relative directory: "inputs/kanjidic2.xml".
The xml file is available at http://www.edrdg.org/kanjidic/kanjidic2.xml.gz

Attribution/Credits
----
- ASCII bar charts:
    - https://alexwlchan.net/2018/05/ascii-bar-charts/
- Kanji grade learned (漢字別漢字配当表) and stroke count data:
    - Electronic Dictionary Research and Development Group, KANJIDIC dictionary file: https://www.edrdg.org/wiki/index.php/Main_Page#The_KANJIDIC_Project

Future Considerations
----
- Determining word boundaries for Japanese text? (e.g. 国勢調査 > 国勢　調査)
- Time series correlation between Nikkei 225 and sentiment of characters
- Similarity between most frequent characters across newspapers (and countries)
- Modeling kanji occurence or stroke count with distributions (e.g. negative hypergeometric: https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.97.7878&rep=rep1&type=pdf)
