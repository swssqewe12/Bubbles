from Particle import *

class Particles:
	def __init__(self):
		self.to_add = []

	def add(self, image, transform, lifetime=1):
		self.to_add.append((image, transform, lifetime))

	def generate(self):
		particles = []
		for image, transform, lifetime in self.to_add:
			particles.append(Particle(image, transform, lifetime))

		self.to_add = []
		return particles