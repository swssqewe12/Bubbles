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
					if dcontrol.recovery_time_left == 0:
						dcontrol.recovery_time_left = dcontrol.recovery_time
						dcontrol.dash_time_left = dcontrol.dash_time
						dcontrol.accel_time_left = dcontrol.accel_time
						dcontrol.particle_time_left = dcontrol.particle_time
						dcontrol.next_particle_interval = dcontrol.particle_interval
						mcontrol.max_speed = dcontrol.max_speed
						mcontrol.accel_speed = dcontrol.accel_speed
				else:
					pass
					# Spot dodge

			# Dash
			if dcontrol.particle_time_left > 0:
				dcontrol.particle_time_left -= dt
			
			if dcontrol.next_particle_interval > 0:
				dcontrol.next_particle_interval = max(0, dcontrol.next_particle_interval - dt)

				if dcontrol.next_particle_interval == 0 and dcontrol.particle_time_left >= 0 and particles is not None:
					dcontrol.next_particle_interval = dcontrol.particle_interval
					pos = transform.pos.added_to(Vector(random.random() * 40 - 20, random.random() * 40 - 20))
					vel = motion.acceleration.normalized().mul_scalar(-dcontrol.particle_speed)
					particles.add("dashcloud", Transform(pos, 1), lifetime=dcontrol.particle_lifetime, velocity=vel)

			if dcontrol.recovery_time_left > 0:
				dcontrol.recovery_time_left = max(0, dcontrol.recovery_time_left - dt)

			if dcontrol.dash_time_left > 0:
				dcontrol.dash_time_left = max(0, dcontrol.dash_time_left - dt)

				if dcontrol.dash_time_left == 0:
					mcontrol.max_speed = mcontrol.initial_max_speed

			if dcontrol.accel_time_left > 0:
				dcontrol.accel_time_left = max(0, dcontrol.accel_time_left - dt)

				if dcontrol.accel_time_left == 0:
					mcontrol.accel_speed = mcontrol.initial_accel_speed