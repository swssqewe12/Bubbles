import esp
from Transform import *
from PlayerTag import *

class GameCameraMovementSystem(esp.Processor):
	
	def __init__(self, camera):
		self.camera = camera
		self.camera.lerp_speed = 0.002
		self.camera.min_zoom = 0.4
		self.camera.max_zoom = 0.8

	def update(self, dt):
		
		box_pos1 = None
		box_pos2 = None

		for ent, (transform, _) in self.world.get_components(Transform, PlayerTag):
			if not box_pos1 or not box_pos2:
				box_pos1 = transform.pos.copy()
				box_pos2 = transform.pos.copy()

			if transform.pos.x < box_pos1.x:
				box_pos1.x = transform.pos.x
			if transform.pos.y < box_pos1.y:
				box_pos1.y = transform.pos.y
				
			if transform.pos.x > box_pos2.x:
				box_pos2.x = transform.pos.x
			if transform.pos.y > box_pos2.y:
				box_pos2.y = transform.pos.y

		box_pos1 = box_pos1 or Vector(0, 0)
		box_pos2 = box_pos2 or Vector(0, 0)

		box_center = box_pos1.added_to(box_pos2).div_scalar(2)
		box_size = box_pos2.subbed_by(box_pos1).mul_scalar(1.4)
		self.camera.target_zoom = self.camera.get_zoom_from_size(box_size)
		self.camera.target_pos = box_center