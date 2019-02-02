import pymorphy2 as pmh
from .yargy_rules import Parser, ATTRIBUTE
import os


class Goods(object):
    def __init__(self, intent: str):
        self.analyzer = pmh.MorphAnalyzer()
        self.goods = []
        self.paths = {
            "sport" : os.path.join(os.path.join(os.path.join('data'), 'sport'), 'slots.csv'),
            "food" : os.path.join(os.path.join(os.path.join('data'), 'food'), 'slots.csv'),
            #"sport" : "..//..//data//sport//slots.csv",
            #"food" : "..//..//data//food//slots.csv"
        }
        self.parse(self.paths[intent], ' ')
    def __getitem__(self, key):
        return self.goods[int(key)]
    #@overrides
    def parse(self, file : str, bracket : str):
        with open(file, "r", encoding='utf-8') as file:
            parser = Parser(ATTRIBUTE)
            for line in file:
                line = line.replace('\n', '')
                for match in parser.findall(line):
                    for token in match.tokens:
                        self.goods.append(token.value)
        #исключаем повторы
        self.goods = list(set(self.goods))
        #print(self.goods)
