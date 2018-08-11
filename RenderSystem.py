import esp
from Transform import *
from Renderable import *
from Sprite import *

class RenderSystem(esp.Processor):

	def draw(self):
		for ent, (transform, rend) in self.world.get_components(Transform, Renderable):
			for _, sprite in rend.sprite_list.items():
				self.handle_todo(sprite, sprite.todo)
				sprite.todo = []
				sprite.prepare_render(transform, rend.camera)

		Sprite.SPRITE_BATCH.draw()

	def handle_todo(self, sprite, todo):
		#TODO: move inside Sprite class
		for data in todo:
			if data["name"] == "set_image":
				sprite._spr.image = data["image"]
			elif data["name"] == "set_visible":
				sprite._spr.visible = data["value"]
			elif data["name"] == "_create_internal_sprite":		
				sprite._spr = sprite.pool.create(data["image"])
			elif data["name"] == "_delete_internal_sprite":		
				sprite.pool.remove(sprite._spr)