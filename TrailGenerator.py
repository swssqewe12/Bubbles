import esp
from Transform import *
from Renderable import *
from Trail import *
from Sprite import *

class TrailGenerator(esp.Processor):

	def update(self, dt):

		for ent, (transform, rend, trail) in self.world.get_components(Transform, Renderable, Trail):

			for handle in trail.list:
				sprite = rend.get_sprite(handle)
				sprite.transform.scale -= ((trail.max_trail_scale - trail.min_trail_scale) / trail.trail_lifetime) * dt
				sprite.opacity -= (1 / trail.trail_lifetime) * dt

			oldest_handle = trail.get_oldest()
			if oldest_handle:
				oldest_sprite = rend.get_sprite(oldest_handle)
				if oldest_sprite.opacity <= 0:
					trail.pop_oldest()
					rend.remove_sprite(oldest_handle)

			create_tail = False
			newest_handle = trail.get_newest()

			if newest_handle:
				newest_sprite = rend.get_sprite(newest_handle)
				dist = transform.pos.subbed_by(newest_sprite.get_absolute_pos(transform.pos)).magnitude()
				if dist >= trail.next_trail_distance:
					create_tail = True
			else:
				create_tail = True

			if create_tail:
				handle = rend.add_sprite(Sprite("tail", -1, False, Transform(transform.pos.copy(), scale=trail.max_trail_scale)))
				trail.add(handle)