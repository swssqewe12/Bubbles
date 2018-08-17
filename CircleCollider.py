from Collider import *

class CircleCollider(Collider):
	def __init__(self, pos, rad, rel_pos=None):
		self.pos = pos
		self.rad = rad
		self.rel_pos = rel_pos
		if not self.rel_pos: self.rel_pos = lambda x:x

	def __repr__(self):
		return "CircleCollider(pos=" + str(self.pos) + " rad=" + str(self.rad) + ")"

	def check_CircleCollider(self, other, info):
		pos_diff = self.rel_pos(self.pos).subbed_by(other.rel_pos(other.pos))
		distance = (pos_diff.magnitude()) - (self.rad + other.rad)
		if info:
			info.pos_change_to_touch = pos_diff.normalized().mul_scalar(-distance)
		return distance <= 0