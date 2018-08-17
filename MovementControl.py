class MovementControl:
	def __init__(self):
		self.dir_ic_list = []
		self.ic_sprint = None
		self.accel_speed = 1250
		self.max_speed = 450
		self.initial_scale = 1
		self.sprint_accel_speed = 2500
		self.sprint_max_speed = 600
		self.sprint_scale = 0.92
		self.accel_change_speed = 0.04
		self.curr_accel_scalar = 1
		self.min_accel_scalar = 0.7
		self.is_moving = False
		self.rot = 0
		self.disabled = 0

	def add_dir_control(self, ic, vec):
		self.dir_ic_list.append((ic, vec))
