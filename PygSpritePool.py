import pyglet

class PygSpritePool:
	def __init__(self, batch, group, free_step=10):
		self.free_step = free_step
		self.pool = []
		self.unused = []
		self.unfreed_count = 0
		self.target_batch = batch
		self.target_group = group

	def create(self, img):
		if len(self.unused) == 0:
			spr = pyglet.sprite.Sprite(img, batch=self.target_batch, group=self.target_group)
			self.pool.append(spr)
			spr.__index = len(self.pool) - 1
			return spr
		
		index = self.unused.pop()
		spr = self.pool[index]

		if not spr:
			spr = pyglet.sprite.Sprite(img, batch=self.target_batch, group=self.target_group)
			self.pool[index] = spr
			spr.__index = index
			return spr

		spr.visible = True
		spr.image = img
		return spr

	def remove(self, spr):
		self.unused.append(spr.__index)
		self.unfreed_count += 1
		if self.unfreed_count >= self.free_step:
			self.unfreed_count -= self.free_step
			self._free()
		else:	
			spr.visible = False

	def _free(self):
		for index in reversed(self.unused):
			if self.pool[index] == None: continue
			self.pool[index].delete()
			self.pool[index] = None

		for spr in reversed(self.pool):
			if spr == None: self.pool.pop()
			else: break

		for index in reversed(self.unused):
			if index >= len(self.pool):
				self.unused.pop(index)