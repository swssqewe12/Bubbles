import res, pyglet
from Transform import *

class Sprite():
	def __init__(self, image_name, z_index=0):
		self._spr = pyglet.sprite.Sprite(res.images[image_name], batch=Sprite.SPRITE_BATCH, group=Sprite.get_group(z_index))
		self.transform = Transform()

	def set_image(self, image_name):
		self._spr.image = res.images[image_name]

	def prepare_render(self, transform=Transform(), camera=None):
		pos = transform.pos.added_to(self.transform.pos)
		scale = transform.scale * self.transform.scale
		if camera:
			pos = camera.rv(pos)
			scale = camera.rs(scale)
		self._spr.position = pos.x, pos.y
		self._spr.scale = scale

	@staticmethod
	def get_group(z_index):
		group = Sprite.sprite_groups.get(z_index, None)
		if not group:
			group = pyglet.graphics.OrderedGroup(z_index)
			Sprite.sprite_groups[z_index] = group
		return group
	
	sprite_groups = {}
	SPRITE_BATCH = pyglet.graphics.Batch()