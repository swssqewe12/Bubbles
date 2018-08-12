import esp, math, mathutils, random
from Transform import *
from Motion import *
from DashControl import *
from MovementControl import *
from Particles import *
from Vector import *

class DashInputSystem(esp.Processor):

	def update(self, dt):
		for ent, (transform, motion, mcontrol, dcontrol) in self.world.get_components(Transform, Motion, MovementControl, DashControl):
			particles = self.world.get_entity_component(ent, Particles)

			if dcontrol.ic.get_amt() > 0:
				if mcontrol.is_moving and (motion.velocity.x != 0 or motion.velocity.y != 0):
					# Dash
					if dcontrol.curr_recovery_time == 0:
						dcontrol.curr_recovery_time = dcontrol.recovery_time
						dcontrol.curr_dash_time = dcontrol.dash_time
						dcontrol.curr_accel_time = dcontrol.accel_time
						dcontrol.curr_dashcloud_generation_time = dcontrol.dashcloud_generation_interval
						mcontrol.max_speed = dcontrol.max_speed
						mcontrol.accel_speed = dcontrol.accel_speed
						#diff = dcontrol.added_speed / motion.velocity.magnitude()
						#motion.velocity.mul_scalar(diff)
				else:
					pass
					# Spot dodge

			# Dash
			if dcontrol.curr_dashcloud_generation_time > 0:
				dcontrol.curr_dashcloud_generation_time -= dt
				dcontrol.curr_dashcloud_generation_time = max(0, dcontrol.curr_dashcloud_generation_time)

			if dcontrol.curr_recovery_time > 0:
				dcontrol.curr_recovery_time -= dt
				dcontrol.curr_recovery_time = max(0, dcontrol.curr_recovery_time)

			if dcontrol.curr_dash_time > 0:
				dcontrol.curr_dash_time -= dt
				dcontrol.curr_dash_time = max(0, dcontrol.curr_dash_time)

				if dcontrol.curr_dash_time == 0:
					mcontrol.max_speed = mcontrol.initial_max_speed

			if dcontrol.curr_accel_time > 0:
				dcontrol.curr_accel_time -= dt
				dcontrol.curr_accel_time = max(0, dcontrol.curr_accel_time)

				if dcontrol.curr_accel_time == 0:
					mcontrol.accel_speed = mcontrol.initial_accel_speed

				if dcontrol.curr_dashcloud_generation_time == 0 and particles is not None:
					dcontrol.curr_dashcloud_generation_time = dcontrol.dashcloud_generation_interval
					pos = transform.pos.added_to(Vector(random.random() * 10 - 5, random.random() * 10 - 5))
					particles.add("dashcloud", Transform(pos, 1))