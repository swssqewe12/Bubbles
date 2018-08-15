class CircleCollider:
	def __init__(self, pos, rad, rel_pos=None, entity=None):
		self.pos = pos
		self.rad = rad
		self.rel_pos = rel_pos
		if not self.rel_pos: self.rel_pos = lambda x:x
		self.on_collision = lambda *args,**kwargs: None
		self.entity = entity

	def __repr__(self):
		return "CircleCollider(pos=" + str(self.pos) + " rad=" + str(self.rad) + ")"

	def check_CircleCollider(self, other):
		return self.rel_pos(self.pos).subbed_by(other.rel_pos(other.pos)).magnitude() <= self.rad + other.rad