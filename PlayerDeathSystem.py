import esp

# Components
from Transform import *
from Motion import *
from PlayerTag import *

class PlayerDeathSystem(esp.Processor):

	def __init__(self, camera, boundary):
		self.camera = camera
		self.boundary_div_2 = boundary.dived_by_scalar(2)

	def update(self, dt):
		for ent, (transform, motion, _) in self.world.get_components(Transform, Motion, PlayerTag):
			if (transform.pos.x < self.camera.pos.x - self.boundary_div_2.x or
				transform.pos.x > self.camera.pos.x + self.boundary_div_2.x or
				transform.pos.y < self.camera.pos.y - self.boundary_div_2.y or
				transform.pos.y > self.camera.pos.y + self.boundary_div_2.y):

				transform.pos.x, transform.pos.y = (self.camera.pos.x, self.camera.pos.y)
				motion.velocity.clear()
				motion.acceleration.clear()