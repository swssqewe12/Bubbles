import esp
from Transform import *
from Renderable import *
from Particles import *
from Sprite import *

class RenderSystem(esp.Processor):
	
	def __init__(self):
		self.particles = []

	def update(self, dt):		
		for ent, particles in self.world.get_component(Particles):
			self.particles += particles.generate()

		for particle in self.particles:
			particle.update(dt)

	def draw(self):
		to_delete = []

		for ent, (transform, rend) in self.world.get_components(Transform, Renderable):
			for handle, sprite in rend.sprite_list.items():
				sprite.prepare_render(transform, rend.camera)
				if not sprite.is_alive():
					to_delete.append((handle, sprite))
		
		for handle, sprite in to_delete:
			del rend.sprite_list[handle]

		for i in reversed(range(len(self.particles))):
			particle = self.particles[i]
			particle.prepare_render(rend.camera)
			if not particle.is_alive():
				self.particles.pop(i)

		Sprite.SPRITE_BATCH.draw()