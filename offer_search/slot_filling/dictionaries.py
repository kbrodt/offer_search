import pymorphy2 as pmh


class Goods(object):
    def __init__(self, intent: int):
        self.analyzer = pmh.MorphAnalyzer()
        self.goods = [
            "велик",
            "велосипед"
        ]
        self.paths = [
            "..//..//data//sport//slots.csv",
            "..//..//data//food//slots.csv"
        ]
        self.parse(self.paths[int(intent)], ' ')
    def __getitem__(self, key):
        return self.goods[int(key)]
    #@overrides
    def parse(self, file : str, bracket : str):
        #bracket - символ, отделяющий название от описания
        with open(file, "r", encoding='utf-8') as file:
            for line in file:
                line = line.replace('\n', '')
                words = line.split(bracket)
                for word in words:
                    tokens = self.analyzer.parse(word)
                    for token in tokens:
                        self.goods.append(token.normal_form)
        #исключаем повторы
        self.goods = list(set(self.goods))
