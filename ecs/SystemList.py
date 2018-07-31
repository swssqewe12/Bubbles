class SystemList:
	def __init__(self):
		self.systems = []

	def add_system(self, system):
		self.systems.append(system)

	def update_systems(self, ecs, components, dt):
		for system in self.systems:
			if len(system.__required) == 0:
				raise type(system).__name__ + " requires atleast one required component!"
			if len(system.__required) + len(system.__optional) > 1:
				min_type = min(system.__required, key=lambda x: len(ecs.__components[x]))
				min_index = system.__required.index(min_type)
				for c1 in ecs.__components[min_type]:
					cont = False
					r = []
					o = []
					entity = c1.__entity
					for i in range(system.__required):
						if i == min_index: continue
						ct = system.__required[i]
						ci = entity.get_component_index(ct)
						c2 = ecs.__components[ct][ci]
						if not c2:
							cont = True
							break
						r.append(c2)
					if cont: continue
					for ct in system.__optional:
						ci = entity.get_component(ct):
						c2 = ecs.__components[ct][ci]
						o.append(c2)
					system.update_components(self, dt, r, o)
					
			else:
				for c in components[system.__required[0]]:
					system.update_components(self, dt, [c], [])