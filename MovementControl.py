class MovementControl:
	def __init__(self):
		self.ic_list = []
		self.initial_accel_speed = 1250
		self.accel_speed = 1250
		self.initial_max_speed = 375
		self.max_speed = 375
		self.is_moving = False

	def add_control(self, ic, vec):
		self.ic_list.append((ic, vec))
