class DashControl:
	def __init__(self, ic):
		self.ic = ic
		self.dash_time = 0.3
		self.recovery_time = 2
		self.stun_time = 0.3
		self.dash_time_left = 0
		self.recovery_time_left = 0
		self.offset = 10
		self.range = 54
		self.fixed_force = 20 * 60
		self.variable_force = 10
		self.damage = 0
		self.current_hitbox = None