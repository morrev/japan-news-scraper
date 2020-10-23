japan-news-scraper
==========

Simple study aid to display daily headlines, most frequent kanji, and highest difficulty kanji (weighted by grade level, with option to weight by stroke count). 

Running
----
``` python
python scraper.py --display==True
```

Current functionality
----
![Example](/images/example2.png)
### WIP
``` python
```

Attribution/Credits
----
- ASCII bar charts:
    - https://alexwlchan.net/2018/05/ascii-bar-charts/
- Kanji grade learned (漢字別漢字配当表) and stroke count data:
    - Electronic Dictionary Research and Development Group, KANJIDIC dictionary file: https://www.edrdg.org/wiki/index.php/Main_Page#The_KANJIDIC_Project

Future considerations
----
- Speeding up performance of (or eliminating) lxml search of kanji grade/stroke counts
- Converting kanji to classes with instance variables (stroke count, grade, freq, etc.)
- Determining word boundaries for Japanese text? (e.g. 国勢調査 > 国勢　調査)
- Time series correlation between Nikkei 225 and sentiment of characters
- Similarity between most frequent characters across newspapers (and countries)
