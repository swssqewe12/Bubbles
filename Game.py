import pyglet, esp, constants
from pyglet.window import key

from RenderSystem import *
from MovementInputSystem import *
from ICController import *

# Temporary imports
from Camera import *
from Transform import *
from Renderable import *
from Vector import *
from Sprite import *
from MovementControl import *
from InputControl import *
from PhysicsSystem import *

class Game(pyglet.window.Window):
	def __init__(self):
		self.init_window()
		self.init_controller()
		self.init_world()
		self.init_systems()
		self.init_entities()
		self.fixed_update_additional_dt = 0

	def init_window(self):
		config = pyglet.gl.Config(sample_buffers=1, samples=constants.SAMPLES) if constants.SAMPLES > 1 else pyglet.gl.Config(sample_buffers=0)
		super().__init__(config=config, resizable=True, fullscreen=True)

	def init_controller(self):
		self.xmic = InputControl()	# X Movement Input Control
		self.ymic = InputControl()	# Y Movement Input Control
		self.icc = ICController()
		self.icc.add_key_control(key.L			,self.xmic, -1)
		self.icc.add_key_control(key.APOSTROPHE	,self.xmic,  1)
		self.icc.add_key_control(key.P			,self.ymic,  1)
		self.icc.add_key_control(key.SEMICOLON	,self.ymic, -1)

	def init_world(self):
		self.world = esp.World()
		self.pgs = {
			"DRAW":			self.world.create_processor_group(),
			"UPDATE":		self.world.create_processor_group(),
			"FIXED_UPDATE":	self.world.create_processor_group()
		}

	def init_systems(self):
		self.world.add_processor(RenderSystem(),		groups=[self.pgs["DRAW"]])
		self.world.add_processor(MovementInputSystem(),	groups=[self.pgs["UPDATE"]])
		self.world.add_processor(PhysicsSystem(),		groups=[self.pgs["FIXED_UPDATE"]])

	def init_entities(self):
		camera = Camera(constants.VIRTUAL_WIDTH)
		screen_size = self.get_size()
		camera.size = Vector(screen_size[0], screen_size[1])
		rend = Renderable()
		rend.add_sprite(Sprite("head"))
		rend.camera = camera
		control = MovementControl()
		control.add_control(self.xmic, Vector(1, 0))
		control.add_control(self.ymic, Vector(0, 1))
		entity = self.world.create_entity(Transform(), Motion(), rend, control)

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

	def on_key_press(self, symbol, modifiers):
		if symbol == key.ESCAPE:
			self.close()
			pyglet.app.exit()
			exit(0)

		self.icc.on_key_down(symbol, modifiers)

	def on_key_release(self, symbol, modifiers):
		self.icc.on_key_up(symbol, modifiers)