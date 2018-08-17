import esp, controller_profiles, pyglet, functools, mathutils
from PygletICCBinder import *
from PlayerICCUnit import *
from Vector import *
from Sprite import *
from BubbleSprite import *
from CircleCollider import *
from Hurtbox import *

# Components
from AttackBoxes import *
from BoostControl import *
from Bubble import *
from Collidable import *
from DashControl import *
from DodgeControl import *
from Motion import *
from MovementControl import *
from Particles import *
from PlayerTag import *
from Renderable import *
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
				icc, ic_x, ic_y, ic_dash = controller_profiles.build_player_controller_icc(player.controller_profile)
				player.pyglet_controller.push_handlers(PygletICCBinder(icc))
				player.controller_icc = icc
				self.create_player_entity(ic_x, ic_y, ic_dash)

	def create_player_entity(self, ic_x, ic_y, ic_dash):
		transform = Transform()
		rend = Renderable()
		head_spr = Sprite("head")
		head = rend.add_sprite(head_spr)
		rend.camera = self.camera
		mcontrol = MovementControl()
		mcontrol.add_control(ic_x, Vector(1, 0))
		mcontrol.add_control(ic_y, Vector(0, 1))
		bcontrol = BoostControl(ic_dash)
		#dodge = DodgeControl(ic_dash)
		#dodge.sprite_handles.append(head)
		dash = DashControl(ic_dash)
		# swoosh
		bubble = Bubble()
		bubble.camera = self.camera
		attack_boxes = AttackBoxes()
		attack_boxes.hurtboxes.append(Hurtbox(CircleCollider(Vector(0, 0), 64, rel_pos=lambda pos: transform.pos.added_to(pos))))
		head_sbo = 64 + 63
		bubble.add_bubble_sprite(BubbleSprite("head", 2, sbo=head_sbo,
			scale_func	 = lambda x,y: head_spr.transform.scale,
			opacity_func = lambda x,y: head_spr.opacity))
		bubble.add_bubble_sprite(BubbleSprite("offscreen_bubble", 1, sbo=112.5,
			scale_func	 = lambda x,y: head_spr.transform.scale,
			opacity_func = lambda x,y: 0.8,
			rot_func	 = lambda bub_spr,_: mathutils.DEG_180-Vector(bub_spr.offscreen_x, bub_spr.offscreen_y).to_rot()+mathutils.DEG_90))
		bubble.roo = 64
		bubble.sprites_to_set_invisible.append(head_spr)
		col = Collidable([
			CircleCollider(Vector(0, 0), 64, rel_pos=lambda pos: transform.pos.added_to(pos))
		])
		col.bounce = 0.2
		entity = self.world.create_entity(PlayerTag(), transform, Motion(), Trail(), Particles(), rend, mcontrol, bcontrol, bubble, dash, attack_boxes, col)