class Damage:
	def __init__(self):
		self.amt = 0

	def get_force(self, fixed_force, variable_force):
		return fixed_force + self.amt / 100 * variable_force