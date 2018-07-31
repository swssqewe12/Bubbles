class System:
	def __init__(self):
		self.__required = []
		self.__optional = []

	def add_required_component(self, typ):
		self.__required.append(typ)
		
	def add_optional_component(self, typ):
		self.__optional.append(typ)

	def update_components(self, _, _, _):
		pass