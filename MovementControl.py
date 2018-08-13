class MovementControl:
	def __init__(self):
		self.ic_list = []
		self.accel_speed = 1250
		self.max_speed = 375
		self.is_moving = False
		self.rot = 0
		self.disabled = 0

	def add_control(self, ic, vec):
		self.ic_list.append((ic, vec))
