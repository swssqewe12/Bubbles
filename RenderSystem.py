import esp
from Transform import *
from Renderable import *
from Sprite import *

class RenderSystem(esp.Processor):

	def draw(self):
		for ent, (transform, rend) in self.world.get_components(Transform, Renderable):
			for sprite in rend.sprite_list:
				sprite.prepare_render(transform, rend.camera)

		Sprite.SPRITE_BATCH.draw()