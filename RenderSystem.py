import esp
from Transform import *
from Renderable import *
from Sprite import *

class RenderSystem(esp.Processor):

	def draw(self):
		for ent, (transform, rend) in self.world.get_components(Transform, Renderable):
			for _, sprite in rend.sprite_list.items():
				sprite.prepare_render(transform, rend.camera)

		Sprite.SPRITE_BATCH.draw()