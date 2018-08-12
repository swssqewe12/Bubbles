import esp, math, mathutils
from Motion import *
from MovementControl import *
from Vector import *

class MovementInputSystem(esp.Processor):

	def update(self, dt):
		for ent, (motion, control) in self.world.get_components(Motion, MovementControl):
			accel = Vector()
			for ic, vec in control.ic_list:
				accel.add(vec.multed_by_scalar(ic.get_amt()))
			control.is_moving = False if accel.x == 0 and accel.y == 0 else True
			
			motion.acceleration = accel.normalize().mul_scalar(control.accel_speed)
			if motion.velocity.magnitude() > control.max_speed:
				motion.velocity.normalize().mul_scalar(control.max_speed)