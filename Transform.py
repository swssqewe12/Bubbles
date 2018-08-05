from Vector import *

class Transform:
	def __init__(self, pos=None, rot=0, scale=1):
		self.pos = pos or Vector()
		self.rot = rot
		self.scale = scale

	def copy(self):
		return Transform(self.pos.copy(), self.rot, self.scale)

	def __repr__(self):
		return "Transform(pos=" + repr(self.pos) + ", rot=" + str(self.rot) + ", scale=" + str(self.scale) + ")"