import esp, mathutils

class CameraLerpSystem(esp.Processor):
	
	def __init__(self, cameras=[]):
		self.cameras = cameras

	def fixed_update(self, dt):
		for camera in self.cameras:
			if camera.lerp_speed > 0:
				camera.zoom = max(min(mathutils.map_range(camera.lerp_speed, 0, 1, camera.zoom, camera.target_zoom), camera.max_zoom), camera.min_zoom)
				camera.pos.x = mathutils.map_range(camera.lerp_speed, 0, 1, camera.pos.x, camera.target_pos.x)
				camera.pos.y = mathutils.map_range(camera.lerp_speed, 0, 1, camera.pos.y, camera.target_pos.y)