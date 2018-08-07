class DashControl:
	def __init__(self, ic):
		self.ic = ic
		self.accel_speed = 10000
		self.max_speed = 1000
		self.recovery_time = 1
		self.dash_time = 0.3
		self.accel_time = 0.15
		self.curr_recovery_time = 0
		self.curr_dash_time = 0
		self.curr_accel_time = 0