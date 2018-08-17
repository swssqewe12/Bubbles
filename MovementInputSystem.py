import esp, math, mathutils
from Motion import *
from MovementControl import *
from Vector import *
from Transform import *

class MovementInputSystem(esp.Processor):

	def update(self, dt):
		for ent, (motion, control) in self.world.get_components(Motion, MovementControl):
			if control.disabled > 0: continue
			transform = self.world.get_entity_component(ent, Transform)
			
			accel = Vector()
			for ic, vec in control.dir_ic_list:
				accel.add(vec.multed_by_scalar(ic.get_amt()))
			control.is_moving = False if accel.x == 0 and accel.y == 0 else True
			control.rot = accel.to_rot()

			if control.ic_sprint.get_amt() == 0:
				accel_speed = control.accel_speed
				max_speed	= control.max_speed
				control.curr_accel_scalar = min(control.curr_accel_scalar + control.accel_change_speed * dt, 1)
				if transform: transform.scale = control.initial_scale
			else:
				print("gywit hwarsht")
				accel_speed = control.sprint_accel_speed
				max_speed	= control.sprint_max_speed
				control.curr_accel_scalar = max(control.curr_accel_scalar - control.accel_change_speed * dt, control.min_accel_scalar)
				if transform: transform.scale = control.sprint_scale
			
			motion.acceleration = accel.set_max_length(1).mul_scalar(accel_speed * control.curr_accel_scalar)
			motion.velocity.set_max_length(max_speed)