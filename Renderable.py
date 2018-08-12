import pyglet

class Renderable:
	def __init__(self):
		self.sprite_list = {}
		self.camera = None

	def add_sprite(self, sprite):
		handle = self._next_sprite_id()
		self.sprite_list[handle] = sprite
		return handle

	def remove_sprite(self, handle):
		self.sprite_list[handle].delete()

	def get_sprite(self, handle):
		return self.sprite_list[handle]

	def _next_sprite_id(self):
		Renderable.next_sprite_id += 1
		return Renderable.next_sprite_id

	def __repr__(self):
		return "Renderable(sprite_count=" + str(len(self.sprite_list)) +")"

	next_sprite_id = 0