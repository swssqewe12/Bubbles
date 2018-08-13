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

						target_accel = motion.velocity.with_length(dcontrol.accel_speed)
						diff = mathutils.rot_diff(motion.velocity.to_rot(), mcontrol.rot)
						if diff > dcontrol.backwards_dash_rot_diff or diff < -dcontrol.backwards_dash_rot_diff:
							target_accel.mul_scalar(-1)
						motion.acceleration = target_accel
						
						if particles:
							# calculations
							d = motion.acceleration.normalized()
							offset = d.rotated(mathutils.HALF_PI).mul_scalar(dcontrol.particle_offset)

							# paramaters
							name = "dashparticle"
							pos = transform.pos#.added_to(d.multed_by_scalar(dcontrol.particle_offset))
							rot = mathutils.HALF_PI - d.to_rot()
							vel = d.mul_scalar(-dcontrol.particle_speed)
							lifetime = dcontrol.particle_lifetime
							opacity_func = lambda x: x

							# creation
							particles.add(name, Transform(pos.added_to (offset), rot + 0.1), lifetime=lifetime, velocity=vel.rotated(-0.2), opacity_func=opacity_func)
							particles.add(name, Transform(pos.subbed_by(offset), rot - 0.1), lifetime=lifetime, velocity=vel.rotated( 0.2), opacity_func=opacity_func)
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