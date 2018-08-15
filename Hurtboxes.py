class Hurtboxes:
	def __init__(self):
		self.to_add = []
		self.to_remove = []
		self.list = []

	def add(self, collider):
		self.to_add.append(collider)
	
	def remove(self, collider):
		self.to_remove.append(collider)