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
						mcontrol.disabled += 1

						'''diff = mathutils.rot_diff(motion.velocity.to_rot(), mcontrol.rot)
						if diff > mathutils.DEG_135 or diff < mathutils.DEG_NEG_135:
							target_accel = Vector.from_rot(mcontrol.rot).mul_scalar(dcontrol.accel_speed)
						else:
							target_accel = motion.velocity.set_length(dcontrol.accel_speed)'''
						motion.acceleration = motion.velocity.with_length(0.9).add(Vector.from_rot(mcontrol.rot).normalize()).set_length(dcontrol.accel_speed)
						
						if particles:
							d = motion.velocity.normalized()
							vel = d.mul_scalar(-dcontrol.particle_speed)
							offset = d.rotated(mathutils.HALF_PI).mul_scalar(dcontrol.particle_offset)
							pos = transform.pos
							particles.add("dashparticle", Transform(pos.added_to(offset), mathutils.HALF_PI - d.to_rot() - 0.2), lifetime=dcontrol.particle_lifetime, velocity=vel.rotated(0.2))
							particles.add("dashparticle", Transform(pos.subbed_by(offset), mathutils.HALF_PI - d.to_rot() + 0.2), lifetime=dcontrol.particle_lifetime, velocity=vel.rotated(-0.2))
				else:
					pass
					# Spot dodge

			# Dash

			if dcontrol.recovery_time_left > 0:
				dcontrol.recovery_time_left = max(0, dcontrol.recovery_time_left - dt)

			if dcontrol.dash_time_left > 0:
				dcontrol.dash_time_left = max(0, dcontrol.dash_time_left - dt)

				if dcontrol.dash_time_left == 0:
					mcontrol.disabled -= 1

			if dcontrol.accel_time_left > 0:
				dcontrol.accel_time_left = max(0, dcontrol.accel_time_left - dt)
				motion.velocity.set_max_length(dcontrol.max_speed)