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
class SportGoods(object):
	def __init__(self):
		self.goods = [
			"qwe"
		]
	def __getitem__(self, key):
		return self.goods[int(key)]

goodsClasses = [
	SportGoods
]

def getGoodsDictionary(type):
	return goodsClasses[type]()