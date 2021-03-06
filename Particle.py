from Sprite import *

class Particle:
	def __init__(self, image, transform, lifetime, velocity, opacity_func):
		self.sprite = Sprite(image, z_index=1, transform=transform)
		self.initial_lifetime = lifetime
		self.lifetime = lifetime
		self.velocity = velocity
		self.opacity_func = opacity_func

	def prepare_render(self, camera):
		self.sprite.prepare_render(camera=camera)
		if not self.sprite.is_alive():
			self.sprite = None

	def update(self, dt):
		self.lifetime -= dt
		if self.lifetime <= 0:
			self.sprite.delete()
		self.sprite.transform.pos.add(self.velocity)
		self.sprite.opacity = self.opacity_func(self.lifetime / self.initial_lifetime)

	def is_alive(self):
		return self.sprite is not None