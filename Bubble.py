class Bubble:
	def __init__(self):
		self.camera = None
		self.bubble_sprites = []
		self.sprites_to_set_invisible = []
		self.sprites_exist = False
		self.roo = 0				# required offscreen offset

	def add_bubble_sprite(self, bubble_sprite):
		self.bubble_sprites.append(bubble_sprite)

	def create_sprites(self, rend):
		for bubble_sprite in self.bubble_sprites:
			bubble_sprite.create_sprite(rend)
		self.sprites_exist = True

	def destroy_sprites(self, rend):
		for bubble_sprite in self.bubble_sprites:
			bubble_sprite.destroy_sprite(rend)
		self.sprites_exist = False