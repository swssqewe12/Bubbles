import esp
from Transform import *
from Motion import *

class PhysicsSystem(esp.Processor):

	def fixed_update(self, dt):

		for ent, (transform, motion) in self.world.get_components(Transform, Motion):
			motion.velocity.add(motion.acceleration.multed_by_scalar(dt))
			transform.pos.add(motion.velocity.multed_by_scalar(dt))