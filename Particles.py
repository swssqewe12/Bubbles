class Particles:
	def __init__(self):
		self._to_add = []

	def add(self, image, transform):
		self._to_add.append((image, transform))