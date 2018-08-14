import esp
from Renderable import *
from Motion import *
from MovementControl import *
from DodgeControl import *

class DodgeInputSystem(esp.Processor):

	def update(self, dt):
		for ent, (motion, movement, dodge) in self.world.get_components(Motion, MovementControl, DodgeControl):
			rend = self.world.get_entity_component(ent, Renderable)

			if dodge.ic.get_amt() > 0:
				if movement.is_moving and (motion.velocity.x != 0 or motion.velocity.y != 0):
					if dodge.recovery_time_left == 0 and dodge.can_forward_dodge:
						self.dodge(rend, movement, dodge)
				else:
					if dodge.recovery_time_left == 0 and dodge.can_spot_dodge:
						self.dodge(rend, movement, dodge)

			if dodge.recovery_time_left > 0:
				dodge.recovery_time_left = max(0, dodge.recovery_time_left - dt)

			if dodge.dodge_time_left > 0:
				dodge.dodge_time_left = max(0, dodge.dodge_time_left - dt)

				if dodge.dodge_time_left == 0:
					movement.disabled -= 1
					if rend:
						for handle in dodge.sprite_handles:
							rend.get_sprite(handle).opacity = 1


	def dodge(self, rend, movement, dodge):
		dodge.dodge_time_left = dodge.dodge_time
		dodge.recovery_time_left = dodge.recovery_time
		movement.disabled += 1
		if rend:
			for handle in dodge.sprite_handles:
				x = dodge.dodge_time_left / dodge.dodge_time
				rend.get_sprite(handle).opacity = 0.5#x if x >= 0.5 else 1 - x
