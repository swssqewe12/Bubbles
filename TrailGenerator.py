import esp
from Transform import *
from Renderable import *
from Trail import *
from Sprite import *

class TrailGenerator(esp.Processor):

	def update(self, dt):

		for ent, (transform, rend, trail) in self.world.get_components(Transform, Renderable, Trail):

			min_dist, min_dist_sprite = math.inf, None
			for handle in trail.list:
				sprite = rend.get_sprite(handle)
				sprite.transform.scale -= ((trail.max_trail_scale - trail.min_trail_scale) / trail.trail_lifetime) * dt
				sprite.opacity -= (1 / trail.trail_lifetime) * dt
				dist = transform.pos.subbed_by(sprite.get_absolute_pos(transform.pos)).magnitude()
				if dist < min_dist:
					min_dist = dist
					min_dist_sprite = sprite

			if min_dist_sprite and min_dist < trail.next_trail_distance:
				min_dist_sprite.opacity = 1
				min_dist_sprite.transform.scale = trail.max_trail_scale
			else:
				handle = rend.add_sprite(Sprite("tail", -1, False, Transform(transform.pos.copy(), scale=trail.max_trail_scale)))
				trail.add(handle)

			for i in reversed(range(len(trail.list))):
				handle = trail.list[i]
				sprite = rend.get_sprite(handle)
				if sprite.opacity <= 0:
					trail.pop(i)
					rend.remove_sprite(handle)

			'''create_tail = False
			newest_handle = trail.get_newest()

			if newest_handle:
				newest_sprite = rend.get_sprite(newest_handle)
				dist = transform.pos.subbed_by(newest_sprite.get_absolute_pos(transform.pos)).magnitude()
				if dist >= trail.next_trail_distance:
					create_tail = True
			else:
				create_tail = True'''