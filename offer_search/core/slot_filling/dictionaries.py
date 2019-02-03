from pathlib import Path
import pymorphy2 as pmh
from .yargy_rules import Parser, ATTRIBUTE
import os


class Goods(object):
    def __init__(self, intent: str):
        self.analyzer = pmh.MorphAnalyzer()
        self.goods = []

        resource_directory = Path('./resources/slot_filling/')
        self.paths = {
            'sport': resource_directory / 'sport.csv',
            'food': resource_directory / 'food.csv',
        }
        self.parse(self.paths[intent], ' ')
    def __getitem__(self, key):
        return self.goods[int(key)]
    #@overrides
<<<<<<< HEAD:offer_search/slot_filling/dictionaries.py
    def parse(self, file : str, bracket : str):
        with open(file, "r", encoding='utf-8') as file:
=======
    def parse(self, file: Path, bracket: str):
        #bracket - символ, отделяющий название от описания
        with file.open("r", encoding='utf-8') as file:
>>>>>>> develop:offer_search/core/slot_filling/dictionaries.py
            parser = Parser(ATTRIBUTE)
            for line in file:
                line = line.replace('\n', '')
                self.goods.append(line)
                #print(line)
                for match in parser.findall(line):
                    for token in match.tokens:
                        self.goods.append(line[token.span.start:token.span.stop])
                        
        #исключаем повторы
        self.goods = list(set(self.goods))
        #print(self.goods)
