from Vector import *

class Motion:
	def __init__(self, velocity=None, acceleration=None):
		self.velocity = velocity or Vector()
		self.acceleration = acceleration or Vector()
		self.friction = 1.0035