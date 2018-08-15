import esp

# Components
from Hitboxes import *
from Hurtboxes import *

class CollisionSystem(esp.Processor):

	def __init__(self):
		self.hitboxes = []
		self.hurtboxes = []
	
	def update(self, dt):

		for ent, hitboxes in self.world.get_component(Hitboxes):
			for hitbox in hitboxes.to_add:
				self.hitboxes.append(hitbox)
				hitboxes.list.append(hitbox)
			for hitbox in hitboxes.to_remove:
				self.hitboxes.remove(hitbox)
				hitboxes.list.remove(hitbox)
			hitboxes.to_add = []
			hitboxes.to_remove = []

		for ent, hurtboxes in self.world.get_component(Hurtboxes):
			for hurtbox in hurtboxes.to_add:
				self.hurtboxes.append(hurtbox)
				hurtboxes.list.append(hurtbox)
			for hurtbox in hurtboxes.to_remove:
				self.hurtboxes.remove(hurtbox)
				hurtboxes.list.remove(hurtbox)
			hurtboxes.to_add = []
			hurtboxes.to_remove = []

		if len(self.hitboxes) == 0: return

		for hurtbox in self.hurtboxes:
			for hitbox in self.hitboxes:
				if getattr(hitbox, "check_" + hurtbox.__class__.__name__, lambda *args,**kwargs:False)(hurtbox):
					hurtbox.on_collision(hurtbox, hitbox)
					hitbox.on_collision(hitbox, hurtbox)
					
