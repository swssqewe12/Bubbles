import math, res, pyglet
from Transform import *
from PygSpritePool import *

class Sprite():
	def __init__(self, image_name, z_index=0, is_relative=True, transform=None):
		self.todo = []
		self.pool = Sprite.get_pool(z_index)
		self.todo.append({"name": "_create_internal_sprite", "image": res.images[image_name]})
		self.transform = transform or Transform()
		self.is_relative = is_relative
		self.opacity = 1
		self._visibility = 1

	def set_image(self, image_name):
		self.todo.append({"name": "set_image", "image": res.images[image_name]})
		#self._spr.image = res.images[image_name]
	
	def change_visibility(self, value):
		self._visibility += value
		self.todo.append({"name": "set_visible", "value": self._visibility > 0})

	def get_absolute_pos(self, relative_pos=None):
		ret = self.transform.pos
		if relative_pos and self.is_relative:
			ret = ret.added_to(relative_pos)
		return ret

	def prepare_render(self, transform=None, camera=None):
		for data in self.todo:
			if data["name"] == "set_image":
				self._spr.image = data["image"]
			elif data["name"] == "set_visible":
				self._spr.visible = data["value"]
			elif data["name"] == "_create_internal_sprite":		
				self._spr = self.pool.create(data["image"])
			elif data["name"] == "_delete_internal_sprite":
				self.pool.remove(self._spr)
				self._spr = None
		
		self.todo = []
		if self._spr == None: return
		
		if transform is None or not self.is_relative:
			transform = Transform()
		pos = transform.pos.added_to(self.transform.pos)
		scale = transform.scale * self.transform.scale
		rot = transform.rot + self.transform.rot
		if camera:
			pos = camera.rv(pos)
			scale = camera.rs(scale)
			#TODO: rot
		self._spr.position = pos.x, pos.y
		self._spr.scale = scale
		self._spr.opacity = self.opacity * 255
		self._spr.rotation = math.degrees(rot)

	def delete(self):
		self.todo.append({"name": "_delete_internal_sprite"})

	def is_alive(self):
		return self._spr is not None

	@staticmethod
	def get_group(z_index):
		group = Sprite.sprite_groups.get(z_index, None)
		if not group:
			group = pyglet.graphics.OrderedGroup(z_index)
			Sprite.sprite_groups[z_index] = group
		return group

	@staticmethod
	def get_pool(z_index):
		pool = Sprite.sprite_pools.get(z_index, None)
		if not pool:
			pool = PygSpritePool(Sprite.SPRITE_BATCH, Sprite.get_group(z_index))
			Sprite.sprite_pools[z_index] = pool
		return pool
	
	sprite_groups = {}
	sprite_pools = {}
	SPRITE_BATCH = pyglet.graphics.Batch()