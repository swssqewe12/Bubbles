import esp
from CollisionInfo import *

# Components
from Collidable import *
from Motion import *
from Transform import *

class PhysicsSystem(esp.Processor):

	def fixed_update(self, dt):

		for ent, (transform, motion) in self.world.get_components(Transform, Motion):
			motion.velocity.div_scalar(motion.friction)
			motion.velocity.add(motion.acceleration.multed_by_scalar(dt))
			transform.pos.add(motion.velocity.multed_by_scalar(dt))

	def update(self, dt):

		handled = {}

		for ent_a, (transform_a, motion_a, collidable_a) in self.world.get_components(Transform, Motion, Collidable):
			for ent_b, (transform_b, motion_b, collidable_b) in self.world.get_components(Transform, Motion, Collidable):
				if ent_a != ent_b and not handled.get((ent_a, ent_b), False):
					for collider_a in collidable_a.colliders:
						brk = False
						for collider_b in collidable_b.colliders:
							info = CollisionInfo()
							if collider_a.check(collider_b, info):
								vel_mag_a = motion_a.velocity.magnitude()
								vel_mag_b = motion_b.velocity.magnitude()
								if vel_mag_a != 0 and vel_mag_b != 0:
									transform_a.pos.add(info.pos_change_to_touch.multed_by_scalar(vel_mag_a / (vel_mag_a + vel_mag_b)))
									transform_b.pos.sub(info.pos_change_to_touch.multed_by_scalar(vel_mag_b / (vel_mag_a + vel_mag_b)))
									if collidable_a.bounce > 0 or collidable_b.bounce > 0:
										bounce_dir = transform_a.pos.subbed_by(transform_b.pos).normalized()
										a_vel_change = bounce_dir.multed_by_scalar((motion_b.velocity.magnitude() * collidable_a.weight / collidable_b.weight) * collidable_b.bounce)
										b_vel_change = bounce_dir.multed_by_scalar((motion_a.velocity.magnitude() * collidable_a.weight / collidable_b.weight) * collidable_b.bounce * -1)
										motion_a.velocity.add(a_vel_change)
										motion_b.velocity.add(b_vel_change)
										motion_a.velocity.sub(b_vel_change)
										motion_b.velocity.sub(a_vel_change)
								brk = True
							if brk: break
						if brk: break
					handled[(ent_b, ent_a)] = True

