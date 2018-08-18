class Stunnable:
	def __init__(self):
		self.is_stunned = False
		self.prepare_stun = False
		self.stun_time_left = 0

	def stun(self, time):
		if self.stun_time_left == 0: self.prepare_stun = True
		self.stun_time_left = max(self.stun_time_left, time)