import res, pyglet
from Transform import *

class Sprite():
	def __init__(self, image_name, z_index=0, is_relative=True, transform=None):
		if transform is None: transform = Transform()
		self._spr = pyglet.sprite.Sprite(res.images[image_name], batch=Sprite.SPRITE_BATCH, group=Sprite.get_group(z_index))
		self.transform = transform
		self.is_relative = is_relative
		self.opacity = 1

	def set_image(self, image_name):
		self._spr.image = res.images[image_name]

	def set_opacity(self, value):
		self._spr.opacity = value

	def get_opacity(self):
		return self._spr.opacity

	def get_absolute_pos(self, relative_pos=None):
		ret = self.transform.pos
		if relative_pos and self.is_relative:
			ret = ret.added_to(relative_pos)
		return ret

	def prepare_render(self, transform=None, camera=None):
		if transform is None or not self.is_relative:
			transform = Transform()
		pos = transform.pos.added_to(self.transform.pos)
		scale = transform.scale * self.transform.scale
		if camera:
			pos = camera.rv(pos)
			scale = camera.rs(scale)
		self._spr.position = pos.x, pos.y
		self._spr.scale = scale
		self._spr.opacity = self.opacity * 255

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