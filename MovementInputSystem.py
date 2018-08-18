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
				control.curr_max_speed_scalar = min(control.curr_max_speed_scalar + control.max_speed_scalar_change_speed * dt, 1)
				if transform: transform.scale = control.initial_scale
			else:
				accel_speed = control.sprint_accel_speed
				max_speed	= control.sprint_max_speed
				control.curr_max_speed_scalar = max(control.curr_max_speed_scalar - control.max_speed_scalar_change_speed * dt, control.min_max_speed_scalar)
				if transform: transform.scale = control.sprint_scale / mathutils.map_range(control.curr_max_speed_scalar, control.min_max_speed_scalar, 1, control.min_scale_divider, 1)
			
			motion.acceleration = accel.set_max_length(1).mul_scalar(accel_speed)
			motion.velocity.set_max_length(max_speed * control.curr_max_speed_scalar)