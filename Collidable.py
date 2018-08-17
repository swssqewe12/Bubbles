class Collidable:
	def __init__(self, colliders):
		self.colliders = colliders
		self.bounce = 0
		self.weight = 1