class InputControl:
	def __init__(self):
		self.amt = 0.0

	def add_amt(self, x):
		self.amt += x

	def get_amt(self):
		return max(min(self.amt, 1), -1)