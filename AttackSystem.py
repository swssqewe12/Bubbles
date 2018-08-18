import esp, functools

# Components
from AttackBoxes import *
from Motion import *
from MovementControl import *
from Stunnable import *

class AttackSystem(esp.Processor):

	def update(self, dt):
		for ent_a, attack_boxes_a in self.world.get_component(AttackBoxes):
			for hitbox in attack_boxes_a.hitboxes:
				for ent_b, attack_boxes_b in self.world.get_component(AttackBoxes):
					if ent_a == ent_b or hitbox.hit_entities.get(ent_b, False): continue
					for hurtbox in attack_boxes_b.hurtboxes:
						if hitbox.collider.check(hurtbox.collider):
							attack_dir = hitbox.attack_dir(ent_b).normalized()
							motion = self.world.get_entity_component(ent_b, Motion)
							motion.velocity.add(attack_dir.multed_by_scalar(hitbox.fixed_force))
							hitbox.hit_entities[ent_b] = True
							if hitbox.stun_time > 0:
								stunnable = self.world.get_entity_component(ent_b, Stunnable)
								if stunnable:
									stunnable.stun(hitbox.stun_time - dt)
							if hitbox.onhit: hitbox.onhit(ent_b, attack_dir)