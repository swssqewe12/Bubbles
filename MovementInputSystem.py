import esp, math, mathutils
from Motion import *
from MovementControl import *
from Vector import *

class MovementInputSystem(esp.Processor):

	def update(self, dt):
		for ent, (motion, control) in self.world.get_components(Motion, MovementControl):
			'''dir_vec = Vector()
			for ic, vec in control.ic_list:
				dir_vec.add(vec.multed_by_scalar(ic.get_amt()))
			if dir_vec.x == 0 and dir_vec.y == 0:
				control.target_rot = None
				motion.velocity = Vector()
			else:
				control.target_rot = dir_vec.to_rot()
				diff = mathutils.rot_diff(control.target_rot, control.curr_rot)
				rot_speed = control.rot_speed * mathutils.TWO_PI * dt
				rot_speed = rot_speed if diff >= 0 else -rot_speed
				if control.is_rotated:
					diff = min(diff, rot_speed, key=abs)
				print(math.degrees(diff), math.degrees(rot_speed))
				motion.velocity = Vector.from_rot(control.curr_rot + diff).mul_scalar(control.movement_speed)
				control.curr_rot = motion.velocity.to_rot()
				control.is_rotated = True'''
			vel = Vector()
			for ic, vec in control.ic_list:
				vel.add(vec.multed_by_scalar(ic.get_amt()))
			motion.velocity = vel.normalize().mul_scalar(control.movement_speed)