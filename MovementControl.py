class MovementControl:
	def __init__(self):
		self.ic_list = []
		self.accel_speed = 1250
		self.max_speed = 375

	def add_control(self, ic, vec):
		self.ic_list.append((ic, vec))