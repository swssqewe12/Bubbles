import math

class BoostControl:
	def __init__(self, ic):
		self.ic = ic
		self.accel_speed = 10000
		self.max_speed = 1000
		self.recovery_time = 2
		self.boost_time = 0.3
		self.accel_time = 0.15
		self.particle_lifetime = 0.5
		self.particle_speed = 1.5
		self.particle_offset = 50
		self.recovery_time_left = 0
		self.boost_time_left = 0
		self.accel_time_left = 0
		self.particle_time_left = 0
		self.next_particle_interval = 0
		self.back_boost_rot_diff = math.radians(120)