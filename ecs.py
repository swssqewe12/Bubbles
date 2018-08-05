class Component:
	pass



class Entity:
	def __init__(self):
		self._components = []

	def get_component_index(self, typ):
		for c in self._components:
			if c[0] == typ:
				return c[1]



class System:
	def __init__(self):
		self._required = []
		self._optional = []

	def add_required_component(self, typ):
		self._required.append(typ)
		
	def add_optional_component(self, typ):
		self._optional.append(typ)

	def update_components(self, dt, r, o):
		pass



class SystemList:
	def __init__(self):
		self.systems = []

	def add_system(self, system):
		self.systems.append(system)

	def update_systems(self, cl, *args, **kwargs):
		for system in self.systems:
			if len(system._required) == 0:
				raise type(system).__name__ + " requires atleast one required component!"
			if len(system._required) + len(system._optional) > 1:
				min_type = min(system._required, key=lambda x: len(cl._components[x]))
				min_index = system._required.index(min_type)
				for c1 in cl._components[min_type]:
					cont = False
					r = [c1]
					o = []
					entity = c1._entity
					for i in range(len(system._required)):
						if i == min_index: continue
						ct = system._required[i]
						ci = entity.get_component_index(ct)
						c2 = cl._components[ct][ci]
						if not c2:
							cont = True
							break
						r.append(c2)
					if cont: continue
					for ct in system._optional:
						ci = entity.get_component_index(ct)
						c2 = cl._components[ct][ci]
						o.append(c2)
					system.update_components(r, o, *args, **kwargs)
					
			else:
				for c in cl._components[system._required[0]]:
					system.update_components([c], [], *args, **kwargs)



class ComponentList:
	def __init__(self):
		self._components = {}

	def register_component_type(self, typ):
		self._components[typ] = []

	def add_component(self, component, entity):
		component._entity = entity
		self._components[component.__class__].append(component)
		entity._components.append((component.__class__, len(self._components[component.__class__]) - 1))

	def remove_component(self, typ, index):
		if index == len(self.components[typ]) - 1:
			self._components[typ].pop()
		else:
			last = self._components[typ][len(self._components[typ]) - 1]
			self._components[typ][index] = last
			self._components[typ].pop()