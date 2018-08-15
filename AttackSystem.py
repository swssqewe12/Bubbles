import esp, functools

# Components
from AttackBoxes import *
from Motion import *
from MovementControl import *

class AttackSystem(esp.Processor):

	def __init__(self):
		self.timers = []

	def update(self, dt):
		for i in reversed(range(len(self.timers))):
			time_left, func = self.timers[i]
			time_left -= dt
			if time_left <= 0:
				func()
				self.timers.pop(i)
			else:
				self.timers[i] = (time_left, func)

		for ent_a, attack_boxes_a in self.world.get_component(AttackBoxes):
			for hitbox in attack_boxes_a.hitboxes:
				for ent_b, attack_boxes_b in self.world.get_component(AttackBoxes):
					if ent_a == ent_b or hitbox.hit_entities.get(ent_b, False): continue
					for hurtbox in attack_boxes_b.hurtboxes:
						if getattr(hitbox.collider, "check_" + hurtbox.collider.__class__.__name__, lambda *args,**kwargs:False)(hurtbox.collider):
							motion = self.world.get_entity_component(ent_b, Motion)
							motion.velocity.add(hitbox.attack_dir(ent_b).with_length(hitbox.fixed_force))
							hitbox.hit_entities[ent_b] = True
							if hitbox.movement_stun_time > 0:
								movement = self.world.get_entity_component(ent_b, MovementControl)
								if movement:
									movement.disabled += 1
									def enable_movement(movement):
										movement.disabled -= 1
									self.timers.append((hitbox.movement_stun_time, functools.partial(enable_movement, movement)))
