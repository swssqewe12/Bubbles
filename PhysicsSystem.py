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

		for ent_a, (transform_a, motion_a, collidable_a) in self.world.get_components(Transform, Motion, Collidable):
			for ent_b, (transform_b, motion_b, collidable_b) in self.world.get_components(Transform, Motion, Collidable):
				if ent_a != ent_b:
					for collider_a in collidable_a.colliders:
						for collider_b in collidable_b.colliders:
							info = CollisionInfo()
							if collider_a.check(collider_b, info):
								vel_mag_a = motion_a.velocity.magnitude()
								vel_mag_b = motion_b.velocity.magnitude()
								transform_a.pos.add(info.pos_change_to_touch.multed_by_scalar(vel_mag_a / (vel_mag_a + vel_mag_b)))
								transform_b.pos.sub(info.pos_change_to_touch.multed_by_scalar(vel_mag_b / (vel_mag_a + vel_mag_b)))