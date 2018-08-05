import pyglet

class Renderable:
	def __init__(self):
		self.sprite_list = []
		self.camera = None

	def add_sprite(self, sprite):
		self.sprite_list.append(sprite)