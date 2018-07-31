import ecs

class TestComponent(ecs.Component):
	def __init__(self, entity):
		super().__init__(entity)
		print(self._entity)
		self.example = "Hello, World!"

class TestSystem(ecs.System):
	def __init__(self):
		super().__init__()
		self.add_required_component(TestComponent)

	def update_components(self, dt, rcomps, ocomps):
		print(rcomps[0].example)

cl = ecs.ComponentList()
cl.register_component_type(TestComponent)

entity = ecs.Entity()
cl.add_component(TestComponent(entity))

sl = ecs.SystemList()
sl.add_system(TestSystem())
sl.update_systems(cl, 10)