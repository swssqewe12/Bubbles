import esp, math, mathutils, random
from Transform import *
from Motion import *
from BoostControl import *
from MovementControl import *
from Particles import *
from Vector import *

class BoostInputSystem(esp.Processor):

	def update(self, dt):
		for ent, (transform, motion, mcontrol, bcontrol) in self.world.get_components(Transform, Motion, MovementControl, BoostControl):
			particles = self.world.get_entity_component(ent, Particles)

			if bcontrol.ic.get_amt() > 0 and bcontrol.recovery_time_left == 0 and bcontrol.disabled == 0:
				if mcontrol.is_moving and (motion.velocity.x != 0 or motion.velocity.y != 0):
					bcontrol.recovery_time_left = bcontrol.recovery_time
					bcontrol.boost_time_left = bcontrol.boost_time
					bcontrol.accel_time_left = bcontrol.accel_time
					mcontrol.disabled += 1

					target_accel = motion.velocity.with_length(bcontrol.accel_speed)
					diff = mathutils.rot_diff(motion.velocity.to_rot(), mcontrol.rot)
					if diff > bcontrol.back_boost_rot_diff or diff < -bcontrol.back_boost_rot_diff:
						target_accel.mul_scalar(-1)
					motion.acceleration = target_accel
					
					if particles:
						# calculations
						d = motion.acceleration.normalized()
						offset = d.rotated(mathutils.HALF_PI).mul_scalar(bcontrol.particle_offset)

						# paramaters
						name = "boost_particle"
						pos = transform.pos#.added_to(d.multed_by_scalar(bcontrol.particle_offset))
						rot = mathutils.HALF_PI - d.to_rot()
						vel = d.mul_scalar(-bcontrol.particle_speed)
						lifetime = bcontrol.particle_lifetime
						opacity_func = lambda x: x

						# creation
						particles.add(name, Transform(pos.added_to (offset), rot + 0.1), lifetime=lifetime, velocity=vel.rotated(-0.2), opacity_func=opacity_func)
						particles.add(name, Transform(pos.subbed_by(offset), rot - 0.1), lifetime=lifetime, velocity=vel.rotated( 0.2), opacity_func=opacity_func)

			if bcontrol.recovery_time_left > 0:
				bcontrol.recovery_time_left = max(0, bcontrol.recovery_time_left - dt)

			if bcontrol.boost_time_left > 0:
				bcontrol.boost_time_left = max(0, bcontrol.boost_time_left - dt)

				if bcontrol.boost_time_left == 0:
					mcontrol.disabled -= 1

			if bcontrol.accel_time_left > 0:
				bcontrol.accel_time_left = max(0, bcontrol.accel_time_left - dt)
				motion.velocity.set_max_length(bcontrol.max_speed)