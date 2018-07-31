class Entity:
	def __init(self):
		self.__components = []

	def get_component_index(self, typ):
		for c in self.__components:
			if c[0] == typ:
				return c[1]