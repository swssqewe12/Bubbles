from Sprite import *

class BubbleSprite:
	def __init__(self, image, z_index=0, sbo=0, scale_func=lambda *args,**kwargs:1, opacity_func=lambda *args,**kwargs:1, rot_func=lambda *args,**kwargs:0):
		self.image = image
		self.z_index = z_index
		self.scale_func = scale_func
		self.opacity_func = opacity_func
		self.rot_func = rot_func
		self.sprite_handle = None
		self.exists = False
		self.sbo = sbo						# sprite boundary offset

	def create_sprite(self, rend):
		self.sprite_handle = rend.add_sprite(Sprite(self.image, self.z_index, is_relative=False))
		self.exists = True

	def destroy_sprite(self, rend):
		rend.remove_sprite(self.sprite_handle)
		self.sprite_handle = None
		self.exists = False