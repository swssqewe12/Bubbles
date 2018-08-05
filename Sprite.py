import res, pyglet
from Transform import *

class Sprite():
	def __init__(self, image_name, z_index=0, relative=True, transform=None):
		if transform is None: transform = Transform()
		self._spr = pyglet.sprite.Sprite(res.images[image_name], batch=Sprite.SPRITE_BATCH, group=Sprite.get_group(z_index))
		self.transform = transform
		self.relative = relative

	def set_image(self, image_name):
		self._spr.image = res.images[image_name]

	def prepare_render(self, transform=None, camera=None):
		if transform is None or not self.relative:
			transform = Transform()
		pos = transform.pos.added_to(self.transform.pos)
		scale = transform.scale * self.transform.scale
		if camera:
			pos = camera.rv(pos)
			scale = camera.rs(scale)
		self._spr.position = pos.x, pos.y
		self._spr.scale = scale

	def delete(self):
		self._spr.delete()

	@staticmethod
	def get_group(z_index):
		group = Sprite.sprite_groups.get(z_index, None)
		if not group:
			group = pyglet.graphics.OrderedGroup(z_index)
			Sprite.sprite_groups[z_index] = group
		return group
	
	sprite_groups = {}
	SPRITE_BATCH = pyglet.graphics.Batch()