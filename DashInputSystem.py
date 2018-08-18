import esp, functools
from CircleCollider import *
from Hitbox import *
from Hurtbox import *

# Components
from AttackBoxes import *
from BoostControl import *
from DashControl import *
from Motion import *
from MovementControl import *
from Particles import *
from Transform import *

class DashInputSystem(esp.Processor):

	def update(self, dt):
		for ent, (transform, motion, movement, dash, attack_boxes) in self.world.get_components(Transform, Motion, MovementControl, DashControl, AttackBoxes):
			boost = self.world.get_entity_component(ent, BoostControl)
			particles = self.world.get_entity_component(ent, Particles)

			if dash.ic.get_amt() > 0 and dash.recovery_time_left == 0 and dash.disabled == 0:
				if movement.is_moving and (motion.velocity.x != 0 or motion.velocity.y != 0) and (not boost or boost.recovery_time_left > 0):
					dash.dash_time_left = dash.dash_time
					dash.recovery_time_left = dash.recovery_time
					collider = CircleCollider(motion.acceleration.normalized().mul_scalar(dash.offset), dash.range, rel_pos=(lambda transform: lambda pos: transform.pos.added_to(pos))(transform))
					dash.current_hitbox = Hitbox(collider, (lambda transform: lambda target: self.world.get_entity_component(target, Transform).pos.subbed_by(transform.pos))(transform), dash.fixed_force, dash.variable_force, dash.damage, dash.dash_time)
					if particles: dash.current_hitbox.onhit = functools.partial(self.onhit, dash, particles)
					attack_boxes.hitboxes.append(dash.current_hitbox)
					movement.disabled += 1

			if dash.recovery_time_left > 0:
				dash.recovery_time_left = max(0, dash.recovery_time_left - dt)

			if dash.dash_time_left > 0:
				dash.dash_time_left = max(0, dash.dash_time_left - dt)

				if dash.dash_time_left == 0:
					attack_boxes.hitboxes.remove(dash.current_hitbox)
					dash.current_hitbox = None
					movement.disabled -= 1

	def onhit(self, dcontrol, particles, target, attack_dir):
		transform = self.world.get_entity_component(target, Transform)

		# calculations
		offset_a = attack_dir.multed_by_scalar(dcontrol.particle_offset)
		offset_b = offset_a.rotated(mathutils.HALF_PI)

		# paramaters
		name = "boost_particle"
		pos = transform.pos.added_to(offset_a)
		rot = mathutils.HALF_PI - attack_dir.to_rot()
		vel = attack_dir.multed_by_scalar(dcontrol.particle_speed)
		lifetime = dcontrol.particle_lifetime
		opacity_func = lambda x: x

		# creation
		particles.add(name, Transform(pos.added_to (offset_b), rot + 0.0), lifetime=lifetime, velocity=vel.rotated(+0.0), opacity_func=opacity_func)
		particles.add(name, Transform(pos.added_to (offset_b), rot + 0.6), lifetime=lifetime, velocity=vel.rotated(+1.2), opacity_func=opacity_func)
		particles.add(name, Transform(pos.subbed_by(offset_b), rot - 0.0), lifetime=lifetime, velocity=vel.rotated(-0.0), opacity_func=opacity_func)
		particles.add(name, Transform(pos.subbed_by(offset_b), rot - 0.6), lifetime=lifetime, velocity=vel.rotated(-1.2), opacity_func=opacity_func)