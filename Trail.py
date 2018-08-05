class Trail:
	def __init__(self):
		self.list = []
		self.max_trail_count = 8
		self.next_trail_time = 0.4
		self.trail_time_interval = 0.4

	def add(self, handle):
		self.list.insert(0, handle)

	def request_pop(self):
		if len(self.list) < self.max_trail_count: return None
		return self.list.pop()

	def __repr__(self):
		return "Trail(count=" + str(len(self.list)) + ")"