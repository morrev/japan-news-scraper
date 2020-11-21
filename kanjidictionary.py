from lxml import etree
import os
import json

class KanjiDictionary():

    def __init__(self, filepath, input_xml = 'inputs/kanjidic2.xml'):
        self.filepath = filepath
        self.input_xml = input_xml

    def get_dict(self):
        if not os.path.isfile(self.filepath):
            kanji_dict = self.create_dict()
        elif os.path.isfile(self.filepath):
            kanji_dict = self.load_dict()
        return kanji_dict

    def create_dict(self):
        kanji_tree = etree.iterparse(self.input_xml, tag="character")
        kanji_dict = {}

        for action, elem in kanji_tree:
            kanji = elem.find('literal').text
            grade = elem.findtext('misc/grade')
            stroke_count = elem.findtext('misc/stroke_count')
            kanji_dict[kanji] = {'grade': grade, 'stroke_count': stroke_count}
        with open(self.filepath, 'w') as fp:
            json.dump(kanji_dict, fp)
        return kanji_dict

    def load_dict(self):
        with open(self.filepath, 'r') as fp:
            kanji_dict = json.load(fp)
        return kanji_dict

if __name__ == "__main__":
    kanji_dic = KanjiDictionary('inputs/kanjidic2.json').get_dict()
