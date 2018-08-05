import math, mathutils

class Vector:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def add(self, vec):
		self.x += vec.x
		self.y += vec.y
		return self

	def added_to(self, vec):
		return Vector(self.x + vec.x, self.y + vec.y)

	def mul_scalar(self, scalar):
		self.x *= scalar
		self.y *= scalar
		return self

	def multed_by_scalar(self, scalar):
		return Vector(self.x * scalar, self.y * scalar)

	def to_rot(self):
		return mathutils.normalized_rot(math.atan2(self.y, self.x))

	def __repr__(self):
		return "Vector(" + str(self.x) + ", " + str(self.y) + ")"

	@staticmethod
	def from_rot(rad):
		rad = mathutils.normalized_rot(rad)
		if rad > math.pi:
			rad -= mathutils.TWO_PI
		return Vector(math.cos(rad), math.sin(rad))