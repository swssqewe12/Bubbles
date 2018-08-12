from Sprite import *

class Particle:
	def __init__(self, image, transform, lifetime):
		self.sprite = Sprite(image, z_index=1, transform=transform)
		self.lifetime = lifetime

	def prepare_render(self, camera):
		self.sprite.prepare_render(camera=camera)
		if not self.sprite.is_alive():
			self.sprite = None

	def update(self, dt):
		self.lifetime -= dt
		if self.lifetime <= 0:
			self.sprite.delete()

	def is_alive(self):
		return self.sprite is not None