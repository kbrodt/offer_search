from string import ascii_letters



class SportGoods(object):
	def __init__(self):
		self.goods = [
			"qwe"
		]
	def __getitem__(self, key):
		return self.goods[int(key)]
my_container = MyContainer() 
print(my_container[0])