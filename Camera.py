from Vector import *

class Camera:
	def __init__(self, vw):
		self.vw = vw
		self.zoom = 1
		self.size = Vector(0, 0)
	
	def rv(self, vec):
		return Vector((vec.x / self.vw) * self.size.x, (vec.y / self.vw) * self.size.x).mul_scalar(self.zoom).add(self.size.multed_by_scalar(0.5))

	def rs(self, scale):
		return scale * (self.size.x / self.vw) * self.zoom