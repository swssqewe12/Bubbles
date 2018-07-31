class ECS:
	def __init__(self):
		self.components = {}

	def register_component_type(typ):
		self.components[typ] = []

	def add_component(component):
		self.components[component.__class__].append(component)
		component.__entity.__components.append((component.__class__, len(self.components[component.__class__]) - 1))

	def remove_component(typ, index):
		if index == len(self.components[typ]) - 1:
			self.components[typ].pop()
		else:
			last = self.components[typ][len(self.components[typ]) - 1]
			self.components[typ][index] = last
			self.components[typ].pop()
