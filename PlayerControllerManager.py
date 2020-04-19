import esp, controller_profiles, pyglet, functools, mathutils
from PygletICCBinder import *
from PlayerICCUnit import *
from EntityFactory import *

# Components
from AttackBoxes import *
from BoostControl import *
from Bubble import *
from Collidable import *
from Damage import *
from DashControl import *
from DodgeControl import *
from Motion import *
from MovementControl import *
from Particles import *
from PlayerTag import *
from Renderable import *
from Stunnable import *
from Trail import *
from Transform import *

class PlayerControllerManager(esp.Processor):

	def __init__(self, keyboard, camera):
		self.camera = camera
		self.player_list = []

		icc, connect_ic = controller_profiles.build_player_connect_icc(controller_profiles.keyboard_player_connect)
		keyboard.push_handlers(PygletICCBinder(icc))
		self.player_list.append(PlayerICCUnit(keyboard, connect_ic, controller_profiles.keyboard_player_controller))

		for joystick in pyglet.input.get_joysticks():
			joystick.open()
			icc, connect_ic = controller_profiles.build_player_connect_icc(controller_profiles.xbox_player_connect)
			joystick.push_handlers(PygletICCBinder(icc))
			self.player_list.append(PlayerICCUnit(joystick, connect_ic, controller_profiles.xbox_player_controller))

	def update(self, dt):
		for player in self.player_list:
			if player.connect_ic.get_amt() > 0 and not player.controller_icc:
				icc, ic_x, ic_y, ic_sprint, ic_dash = controller_profiles.build_player_controller_icc(player.controller_profile)
				player.pyglet_controller.push_handlers(PygletICCBinder(icc))
				player.controller_icc = icc
				EntityFactory.create_player(self.world, self.camera, ic_x, ic_y, ic_sprint, ic_dash)