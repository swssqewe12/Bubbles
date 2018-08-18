class Trail:
	def __init__(self):
		self.list = []
		self.next_trail_distance = 90
		self.trail_lifetime = 0.7
		self.max_trail_scale = 0.70
		self.min_trail_scale = 0.35

	def add(self, handle):
		self.list.insert(0, handle)

	def pop(self, i):
		if len(self.list) > i: 
			return self.list.pop(i)

	def get_newest(self):
		if len(self.list) == 0: return None
		return self.list[0]

	def get_oldest(self):
		if len(self.list) == 0: return None
		return self.list[len(self.list) - 1]

	def __repr__(self):
		return "Trail(count=" + str(len(self.list)) + ")"