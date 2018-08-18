import esp
from CircleCollider import *
from Hitbox import *
from Hurtbox import *

# Components
from Transform import *
from Motion import *
from MovementControl import *
from DashControl import *
from BoostControl import *
from AttackBoxes import *

class DashInputSystem(esp.Processor):

	def update(self, dt):
		for ent, (transform, motion, movement, dash, attack_boxes) in self.world.get_components(Transform, Motion, MovementControl, DashControl, AttackBoxes):
			boost = self.world.get_entity_component(ent, BoostControl)

			if dash.ic.get_amt() > 0 and dash.recovery_time_left == 0 and dash.disabled == 0:
				if movement.is_moving and (motion.velocity.x != 0 or motion.velocity.y != 0) and (not boost or boost.recovery_time_left > 0):
					dash.dash_time_left = dash.dash_time
					dash.recovery_time_left = dash.recovery_time
					collider = CircleCollider(motion.acceleration.normalized().mul_scalar(dash.offset), dash.range, rel_pos=(lambda transform: lambda pos: transform.pos.added_to(pos))(transform))
					dash.current_hitbox = Hitbox(collider, (lambda transform: lambda target: self.world.get_entity_component(target, Transform).pos.subbed_by(transform.pos))(transform), dash.fixed_force, dash.variable_force, dash.damage, dash.dash_time)
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