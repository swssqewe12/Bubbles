import esp
from Transform import *
from Renderable import *
from Trail import *
from Sprite import *

class TrailGenerator(esp.Processor):

	def update(self, dt):

		for ent, (transform, rend, trail) in self.world.get_components(Transform, Renderable, Trail):
			trail.next_trail_time -= dt
			if trail.next_trail_time <= 0:
				handle = rend.add_sprite(Sprite("tail", -1, False, Transform(transform.pos.copy(), scale=0.5)))
				trail.add(handle)
				to_remove = trail.request_pop()
				if to_remove: rend.remove_sprite(to_remove)
				trail.next_trail_time += trail.trail_time_interval