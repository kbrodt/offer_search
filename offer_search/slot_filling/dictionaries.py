'''import abc

__all__ = [
    "Dictionary"
]

class Dictionary(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __getitem__(self, key):
        pass
    @abc.abstractmethod
    def ParseFile(file : str) -> int:
        pass
    
'''
class Goods(object):
    def __init__(self, intent):
        self.goods = [
            "велик"
        ]
    def __getitem__(self, key):
        return self.goods[int(key)]
    #@overrides
    def Parse(self, file, bracket):
        #bracket - символ, отделяющий название от описания
        with open(file, "r") as file:
            for line in file:
                self.goods.append((line)[0])
