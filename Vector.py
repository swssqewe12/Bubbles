import math, mathutils

class Vector:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	# ADD

	def add(self, vec):
		self.x += vec.x
		self.y += vec.y
		return self

	def added_to(self, vec):
		return Vector(self.x + vec.x, self.y + vec.y)

	# SUBTRACT

	def sub(self, vec):
		self.x -= vec.x
		self.y -= vec.y
		return self

	def subbed_by(self, vec):
		return Vector(self.x - vec.x, self.y - vec.y)

	# MULTIPLY

	def mul(self, vec):
		raise NotImplementedError

	def mul_scalar(self, scalar):
		self.x *= scalar
		self.y *= scalar
		return self

	def multed_by(self, vec):
		raise NotImplementedError

	def multed_by_scalar(self, scalar):
		return Vector(self.x * scalar, self.y * scalar)

	# DIVIDE
	
	def div(self, vec):
		raise NotImplementedError
	
	def div_scalar(self, scalar):
		self.x /= scalar
		self.y /= scalar
		return self

	def dived_by(self, vec):
		raise NotImplementedError
		
	def dived_by_scalar(self, scalar):
		raise NotImplementedError

	# NORMALIZE

	def normalize(self):
		mag = self.magnitude()
		if mag == 0: return self
		self.x /= mag
		self.y /= mag
		return self

	def normalized(self):
		raise NotImplementedError

	# MAGNITUDE

	def magnitude(self):
		return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

	# CONVERSIONS

	def to_rot(self):
		return mathutils.normalized_rot(math.atan2(self.y, self.x))

	# OTHER METHODS

	def copy(self):
		return Vector(self.x, self.y)

	def __repr__(self):
		return "Vector(" + str(self.x) + ", " + str(self.y) + ")"

	# STATIC METHODS

	@staticmethod
	def from_rot(rad):
		rad = mathutils.normalized_rot(rad)
		if rad > math.pi:
			rad -= mathutils.TWO_PI
		return Vector(math.cos(rad), math.sin(rad))