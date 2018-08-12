from Particle import *
from Vector import *

class Particles:
	def __init__(self):
		self.to_add = []

	def add(self, image, transform, lifetime=1, velocity=None):
		velocity = velocity or Vector(0, 0, 0)
		self.to_add.append((image, transform, lifetime, velocity))

	def generate(self):
		particles = []
		for image, transform, lifetime, velocity in self.to_add:
			particles.append(Particle(image, transform, lifetime, velocity))

		self.to_add = []
		return particles