import esp
from CircleCollider import *

# Components
from Transform import *
from Motion import *
from MovementControl import *
from DashControl import *
from BoostControl import *
from Hitboxes import *
from PlayerTag import *

class DashInputSystem(esp.Processor):

	def __init__(self):
		self.movements_to_enable = []

	def update(self, dt):
		for ent, (transform, motion, movement, dash, hitboxes) in self.world.get_components(Transform, Motion, MovementControl, DashControl, Hitboxes):
			boost = self.world.get_entity_component(ent, BoostControl)

			if dash.ic.get_amt() > 0 and dash.recovery_time_left == 0:
				if movement.is_moving and (motion.velocity.x != 0 or motion.velocity.y != 0) and (not boost or boost.recovery_time_left > 0):
					dash.dash_time_left = dash.dash_time
					dash.recovery_time_left = dash.recovery_time
					dash.current_collider = CircleCollider(motion.acceleration.normalized().mul_scalar(dash.offset), dash.range, rel_pos=(lambda transform: lambda pos: transform.pos.added_to(pos))(transform), entity=ent)
					dash.current_collider.on_collision = self.create_on_collision_handler(dash, motion)
					hitboxes.add(dash.current_collider)
					movement.disabled += 1

			if dash.recovery_time_left > 0:
				dash.recovery_time_left = max(0, dash.recovery_time_left - dt)

			if dash.dash_time_left > 0:
				dash.dash_time_left = max(0, dash.dash_time_left - dt)

				if dash.dash_time_left == 0:
					hitboxes.remove(dash.current_collider)
					dash.current_collider = None
					movement.disabled -= 1

		for i in reversed(range(len(self.movements_to_enable))):
			movement, time_left = self.movements_to_enable[i]
			time_left -= dt
			if time_left <= 0:
				movement.disabled -= 1
				self.movements_to_enable.pop(i)
			else:
				self.movements_to_enable[i] = (movement, time_left)

	def create_on_collision_handler(self, this_dash, this_motion):
		handled = {}

		def handler(this, target):
			if this.entity != target.entity and not handled.get(target, False):
				handled[target] = True
				if self.world.has_component(target.entity, PlayerTag):
					target_motion = self.world.get_entity_component(target.entity, Motion)
					target_movement = self.world.get_entity_component(target.entity, MovementControl)
					if target_motion:
						target_motion.velocity.add(this_motion.acceleration.normalized().mul_scalar(this_dash.fixed_force))
					if target_movement:
						target_movement.disabled += 1
						self.movements_to_enable.append((target_movement, this_dash.stun_time))
		
		return handler