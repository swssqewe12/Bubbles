import esp, math, mathutils
from Motion import *
from MovementControl import *
from Vector import *

class MovementInputSystem(esp.Processor):

	def update(self, dt):
		for ent, (motion, control) in self.world.get_components(Motion, MovementControl):
			if control.disabled > 0: continue
			
			accel = Vector()
			for ic, vec in control.ic_list:
				accel.add(vec.multed_by_scalar(ic.get_amt()))
			control.is_moving = False if accel.x == 0 and accel.y == 0 else True
			control.rot = accel.to_rot()
			
			motion.acceleration = accel.set_max_length(1).mul_scalar(control.accel_speed)
			motion.velocity.set_max_length(control.max_speed)