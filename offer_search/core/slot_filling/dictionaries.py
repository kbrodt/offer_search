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
    def parse(self, file: Path, bracket: str):
        #bracket - символ, отделяющий название от описания
        with file.open("r", encoding='utf-8') as file:
            parser = Parser(ATTRIBUTE)
            for line in file:
                line = line.replace('\n', '')
                for match in parser.findall(line):
                    for token in match.tokens:
                        self.goods.append(token.value)
        #исключаем повторы
        self.goods = list(set(self.goods))
