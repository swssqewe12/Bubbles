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
				handle = rend.add_sprite(Sprite("tail", -1, False, Transform(transform.pos.copy(), scale=0.75)))
				trail.add(handle)
				to_remove = trail.request_pop()
				if to_remove: rend.remove_sprite(to_remove)
				trail.next_trail_time += trail.trail_time_interval

			for handle in trail.list:
				sprite = rend.get_sprite(handle)
				sprite.transform.scale -= max(0.75 / (trail.max_trail_count * trail.trail_time_interval), 0) * dt
				sprite.opacity -= max(1 / (trail.max_trail_count * trail.trail_time_interval), 0) * dt