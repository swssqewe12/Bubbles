class DodgeControl:
	def __init__(self, ic):
		self.ic = ic
		self.sprite_handles = []
		self.dodge_time = 0.3
		self.recovery_time = 2
		self.dodge_time_left = 0
		self.recovery_time_left = 0
		self.can_spot_dodge = True
		self.can_forward_dodge = True
		