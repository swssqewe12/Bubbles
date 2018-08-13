from Particle import *
from Vector import *

class Particles:
	def __init__(self):
		self.to_add = []

	def add(self, image, transform, lifetime=1, velocity=None, opacity_func=lambda x:1):
		velocity = velocity or Vector(0, 0, 0)
		self.to_add.append((image, transform, lifetime, velocity, opacity_func))

	def generate(self):
		particles = []
		for image, transform, lifetime, velocity, opacity_func in self.to_add:
			particles.append(Particle(image, transform, lifetime, velocity, opacity_func))

		self.to_add = []
		return particles