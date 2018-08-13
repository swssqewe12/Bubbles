import pyglet, esp, constants
from pyglet.window import key

from MovementInputSystem import *
from DashInputSystem import *
from PhysicsSystem import *
from TrailGenerator import *
from RenderSystem import *

from ICController import *

# Temporary imports
from Camera import *
from Transform import *
from Renderable import *
from Vector import *
from Sprite import *
from MovementControl import *
from DashControl import *
from InputControl import *
from Particles import *

class JoystickManager:
	
	def __init__(self, icc):
		self.icc = icc

	def on_joybutton_press(self, joystick, button):
		self.icc.on_joy_btn_down(button)

	def on_joybutton_release(self, joystick, button):
		self.icc.on_joy_btn_up(button)

	def on_joyaxis_motion(self, joystick, axis, value):
		self.icc.on_joy_motion(axis, value)

def xbox_profile(icc, x, y, dash):
	icc.add_joy_motion_control('x', x, (-1,  1), min=0.2)
	icc.add_joy_motion_control('y', y, ( 1, -1), min=0.2)
	icc.add_joy_btn_control(2, dash, 1)

def keyboard_profile(icc, x, y, dash):
	icc.add_key_control(key.L,			x,	  -1)
	icc.add_key_control(key.APOSTROPHE,	x,	   1)
	icc.add_key_control(key.SEMICOLON,	y,	  -1)
	icc.add_key_control(key.P,			y,	   1)
	icc.add_key_control(key.D,			dash,  1)

class Game(pyglet.window.Window):
	def __init__(self):
		self.init_window()
		self.init_controllers()
		self.init_world()
		self.init_systems()
		self.init_entities()
		self.fixed_update_additional_dt = 0

	def init_window(self):
		config = pyglet.gl.Config(sample_buffers=1, samples=constants.SAMPLES) if constants.SAMPLES > 1 else pyglet.gl.Config(sample_buffers=0)
		super().__init__(config=config, resizable=True, fullscreen=True)

	def init_controllers(self):
		self.controllers = []

		connect = InputControl()
		connect_icc = ICController()
		connect_icc.add_key_control(key.A, connect,	1)

		self.controllers.append({
			"profile": keyboard_profile,
			"connect_icc": connect_icc,
			"connect_ic": connect,
			"player_icc": None,
			"joystick": None
		})

		for joystick in pyglet.input.get_joysticks():
			joystick.open()
			connect = InputControl()
			connect_icc = ICController()
			connect_icc.add_joy_btn_control(0, connect, 1)

			self.controllers.append({
				"profile": xbox_profile,
				"connect_icc": connect_icc,
				"connect_ic": connect,
				"player_icc": None,
				"joystick": joystick
			})

			joystick.push_handlers(JoystickManager(connect_icc))
			#joystick.push_handlers(JoystickManager(player_icc))

	def create_ICController(self, profile):
		icc = ICController()

		x		= InputControl()	# X Movement Input Control
		y		= InputControl()	# Y Movement Input Control
		dash 	= InputControl()	# Dash Input Control

		profile(icc, x, y, dash)
		return icc, x, y, dash

	def init_world(self):
		self.world = esp.World()
		self.pgs = {
			"DRAW":			self.world.create_processor_group(),
			"UPDATE":		self.world.create_processor_group(),
			"FIXED_UPDATE":	self.world.create_processor_group()
		}

	def init_systems(self):
		self.world.add_processor(MovementInputSystem(),	groups=[self.pgs["UPDATE"]])
		self.world.add_processor(DashInputSystem(),		groups=[self.pgs["UPDATE"]])
		self.world.add_processor(TrailGenerator(),		groups=[self.pgs["UPDATE"]])
		self.world.add_processor(PhysicsSystem(),		groups=[self.pgs["FIXED_UPDATE"]])
		self.world.add_processor(RenderSystem(),		groups=[self.pgs["UPDATE"], self.pgs["DRAW"]])

	def init_entities(self):
		camera = Camera(constants.VIRTUAL_WIDTH)
		screen_size = self.get_size()
		camera.size = Vector(screen_size[0], screen_size[1])
		self.__temp__camera = camera

	def run(self):
		pyglet.clock.schedule_interval(self.on_update, 1/120.0)

	def on_draw(self):
		pyglet.gl.glClearColor(0.35,0.7,0.7,1)
		self.clear()
		self.world.process_group(self.pgs["DRAW"], method_name="draw")

	def on_update(self, dt):
		self.world.process_group(self.pgs["UPDATE"], dt, method_name="update")
		dt += self.fixed_update_additional_dt
		while dt > 0:
			self.world.process_group(self.pgs["FIXED_UPDATE"], 0.001, method_name="fixed_update")
			dt -= 0.001
		self.fixed_update_additional_dt = dt

		for controller in self.controllers:
			if controller["connect_ic"].get_amt() > 0 and not controller["player_icc"]:
				print("connected!")
				controller["player_icc"], x, y, dash = self.create_ICController(controller["profile"])
				if controller["joystick"]:
					controller["joystick"].push_handlers(JoystickManager(controller["player_icc"]))
				
				rend = Renderable()
				rend.add_sprite(Sprite("head"))
				rend.camera = self.__temp__camera
				mcontrol = MovementControl()
				mcontrol.add_control(x, Vector(1, 0))
				mcontrol.add_control(y, Vector(0, 1))
				dcontrol = DashControl(dash)
				entity = self.world.create_entity(Transform(), Motion(), Trail(), Particles(), rend, mcontrol, dcontrol)



	def on_key_press(self, symbol, modifiers):
		if symbol == key.ESCAPE:
			self.close()
			pyglet.app.exit()
			exit(0)

		for controller in self.controllers:
			controller["connect_icc"].on_key_down(symbol, modifiers)
			if controller["player_icc"]: controller["player_icc"].on_key_down(symbol, modifiers)

	def on_key_release(self, symbol, modifiers):
		for controller in self.controllers:
			controller["connect_icc"].on_key_up(symbol, modifiers)
			if controller["player_icc"]: controller["player_icc"].on_key_up(symbol, modifiers)