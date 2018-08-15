import esp
from Sprite import *

# Components
from Transform import *
from Renderable import *
from Bubble import *

class BubbleGenerator(esp.Processor):

	def update(self, dt):

		for ent, (transform, rend, bubble) in self.world.get_components(Transform, Renderable, Bubble):
			vis_size_div_2 = bubble.camera.get_visible_size().div_scalar(2)

			offscreen_x, offscreen_y = 0, 0

			if transform.pos.x > bubble.camera.pos.x + vis_size_div_2.x + bubble.roo:
				offscreen_x = 1
			elif transform.pos.x < bubble.camera.pos.x - vis_size_div_2.x - bubble.roo:
				offscreen_x = -1

			if transform.pos.y > bubble.camera.pos.y + vis_size_div_2.y + bubble.roo:
				offscreen_y = 1
			elif transform.pos.y < bubble.camera.pos.y - vis_size_div_2.y - bubble.roo:
				offscreen_y = -1
		
			is_offscreen = offscreen_x != 0 or offscreen_y != 0
			
			if is_offscreen and not bubble.sprites_exist:
				bubble.create_sprites(rend)
				for spr in bubble.sprites_to_set_invisible:
					spr.change_visibility(-1)
			elif not is_offscreen and bubble.sprites_exist:
				bubble.destroy_sprites(rend)
				for spr in bubble.sprites_to_set_invisible:
					spr.change_visibility(1)

			if bubble.sprites_exist:
				for bubble_sprite in bubble.bubble_sprites:
					bubble_sprite.offscreen_x = offscreen_x
					bubble_sprite.offscreen_y = offscreen_y
					spr = rend.get_sprite(bubble_sprite.sprite_handle)
					spr.transform.pos.x = min(max(transform.pos.x, bubble.camera.pos.x - vis_size_div_2.x + bubble_sprite.sbo), bubble.camera.pos.x + vis_size_div_2.x - bubble_sprite.sbo)
					spr.transform.pos.y = min(max(transform.pos.y, bubble.camera.pos.y - vis_size_div_2.y + bubble_sprite.sbo), bubble.camera.pos.y + vis_size_div_2.y - bubble_sprite.sbo)
					spr.transform.scale	= bubble_sprite.scale_func(bubble_sprite, spr)
					spr.transform.rot	= bubble_sprite.rot_func(bubble_sprite, spr)
					spr.opacity			= bubble_sprite.opacity_func(bubble_sprite, spr)