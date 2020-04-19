import esp
from EntityFactory import *

# Components
from Transform import *
from Motion import *
from PlayerTag import *

class PlayerDeathSystem(esp.Processor):

	def __init__(self, camera, boundary):
		self.camera = camera
		self.boundary_div_2 = boundary.dived_by_scalar(2)
		self.respawn_time = 5
		self.to_respawn = []

	def update(self, dt):
		for i in reversed(range(len(self.to_respawn))):
			time_left, data = self.to_respawn[i]
			time_left -= dt
			if time_left <= 0:
				self.to_respawn.pop(i)
				ic_x, ic_y, ic_sprint, ic_dash = data
				EntityFactory.create_player(self.world, self.camera, ic_x, ic_y, ic_sprint, ic_dash)
			else:
				self.to_respawn[i] = (time_left, data)
		
		# TODO: allow access to ics without accessing individual components directly
		#		this system shouldn't have to know about movement etc of the entity to handle death and respawn
		for ent, (transform, mcontrol, bcontrol, _) in self.world.get_components(Transform, MovementControl, BoostControl, PlayerTag):
			if (transform.pos.x < self.camera.pos.x - self.boundary_div_2.x or
				transform.pos.x > self.camera.pos.x + self.boundary_div_2.x or
				transform.pos.y < self.camera.pos.y - self.boundary_div_2.y or
				transform.pos.y > self.camera.pos.y + self.boundary_div_2.y):

				EntityFactory.destroy_entity(self.world, ent)
				self.to_respawn.append((self.respawn_time, (mcontrol.dir_ic_list[0][0], mcontrol.dir_ic_list[1][0], mcontrol.ic_sprint, bcontrol.ic)))