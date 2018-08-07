import esp, math, mathutils
from Motion import *
from MovementControl import *
from Vector import *

class MovementInputSystem(esp.Processor):

	def update(self, dt):
		for ent, (motion, control) in self.world.get_components(Motion, MovementControl):
			vel = Vector()
			for ic, vec in control.ic_list:
				vel.add(vec.multed_by_scalar(ic.get_amt()))
			motion.acceleration = vel.normalize().mul_scalar(control.accel_speed)
			if motion.velocity.magnitude() > control.max_speed:
				motion.velocity.normalize().mul_scalar(control.max_speed)