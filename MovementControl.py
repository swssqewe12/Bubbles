class MovementControl:
	def __init__(self):
		self.ic_list = []
		#self.is_rotated = False
		#self.curr_rot = 0
		#self.target_rot = 0
		#self.rot_speed = 1
		self.movement_speed = 50

	def add_control(self, ic, vec):
		self.ic_list.append((ic, vec))