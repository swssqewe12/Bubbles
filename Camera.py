import math
from Vector import *

class Camera:
	def __init__(self, vsize):
		self._vsize = vsize
		self._size = Vector(0, 0)
		self.pos = Vector(0, 0)
		self.zoom = 0.5
		self.min_zoom = 0
		self.max_zoom = math.inf
		self.lerp_speed = 0
		self.target_pos = self.pos
		self.target_zoom = self.zoom

	def set_size(self, size):
		self._size = size
		scalar = self._vsize.x / self._size.x
		x = self._size.y * scalar
		if x > self._vsize.y:
			# x fits
			vnum = self._vsize.x
			rnum = self._size.x
			fits = "x"
		else:
			# y fits
			vnum = self._vsize.y
			rnum = self._size.y
			fits = "y"
		self._vnum = vnum
		self._rnum = rnum
		self._fits = fits
	
	def rv(self, vec):
		return Vector(((vec.x - self.pos.x) / self._vnum) * self._rnum, ((vec.y - self.pos.y) / self._vnum) * self._rnum).mul_scalar(self.zoom).add(self._size.multed_by_scalar(0.5))

	def rs(self, scale):
		return scale * (self._rnum / self._vnum) * self.zoom

	def get_zoom_from_size(self, size):
		return min(math.inf if size.x == 0 else self._vsize.x / size.x, math.inf if size.y == 0 else self._vsize.y / size.y)

	def get_visible_size(self):
		if self._fits == "x":
			a = self._vsize.x / self._size.x
			b = self._vsize.y / self._size.y
			c = b / a
			return Vector(self._vsize.x, self._vsize.y * c)
		
		a = self._vsize.y / self._size.y
		b = self._vsize.x / self._size.x
		c = b / a
		return Vector(self._vsize.x * c / self.zoom, self._vsize.y / self.zoom)