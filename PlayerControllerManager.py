import esp, controller_profiles, pyglet
from PygletICCBinder import *
from PlayerICCUnit import *

# Components
from Vector import *
from Sprite import *
from Transform import *
from Motion import *
from Renderable import *
from MovementControl import *
from BoostControl import *
from DodgeControl import *
from Trail import *
from Particles import *

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
				icc, ic_x, ic_y, ic_dash = controller_profiles.build_player_controller_icc(player.controller_profile)
				player.pyglet_controller.push_handlers(PygletICCBinder(icc))
				player.controller_icc = icc

				rend = Renderable()
				head = rend.add_sprite(Sprite("head"))
				rend.camera = self.camera
				mcontrol = MovementControl()
				mcontrol.add_control(ic_x, Vector(1, 0))
				mcontrol.add_control(ic_y, Vector(0, 1))
				bcontrol = BoostControl(ic_dash)
				dodge = DodgeControl(ic_dash)
				dodge.sprite_handles.append(head)
				entity = self.world.create_entity(Transform(), Motion(), Trail(), Particles(), rend, mcontrol, bcontrol, dodge)