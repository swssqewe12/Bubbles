import pyglet, esp, constants
from pyglet.window import key

# Systems
from PlayerControllerManager import *
from MovementInputSystem import *
from BoostInputSystem import *
from DodgeInputSystem import *
from DashInputSystem import *
from PhysicsSystem import *
from GameCameraMovementSystem import *
from CameraLerpSystem import *
from TrailGenerator import *
from BubbleGenerator import *
from RenderSystem import *
from AttackSystem import *

# Temporary imports
from Camera import *

class Game(pyglet.window.Window):
	def __init__(self):
		self.init_window()
		self.init_cameras()
		self.init_world()
		self.init_systems()
		self.fixed_update_additional_dt = 0

	def init_window(self):
		config = pyglet.gl.Config(sample_buffers=1, samples=constants.SAMPLES) if constants.SAMPLES > 1 else pyglet.gl.Config(sample_buffers=0)
		super().__init__(config=config, resizable=True, fullscreen=True)

	def init_world(self):
		self.world = esp.World()
		self.pgs = {
			"DRAW":			self.world.create_processor_group(),
			"UPDATE":		self.world.create_processor_group(),
			"FIXED_UPDATE":	self.world.create_processor_group()
		}

	def init_systems(self):
		self.world.add_processor(PlayerControllerManager(self, self.game_camera),
			groups=[self.pgs["UPDATE"]])
		self.world.add_processor(MovementInputSystem(),
			groups=[self.pgs["UPDATE"]])
		self.world.add_processor(BoostInputSystem(),
			groups=[self.pgs["UPDATE"]])
		self.world.add_processor(DodgeInputSystem(),
			groups=[self.pgs["UPDATE"]])
		self.world.add_processor(DashInputSystem(),
			groups=[self.pgs["UPDATE"]])
		self.world.add_processor(TrailGenerator(),
			groups=[self.pgs["UPDATE"]])
		self.world.add_processor(BubbleGenerator(),
			groups=[self.pgs["UPDATE"]])
		self.world.add_processor(AttackSystem(),
			groups=[self.pgs["UPDATE"]])
		self.world.add_processor(GameCameraMovementSystem(self.game_camera),
			groups=[self.pgs["UPDATE"]])
		self.world.add_processor(CameraLerpSystem([self.game_camera]),
			groups=[self.pgs["FIXED_UPDATE"]])
		self.world.add_processor(PhysicsSystem(),
			groups=[self.pgs["FIXED_UPDATE"]])
		self.world.add_processor(RenderSystem(),
			groups=[self.pgs["UPDATE"], self.pgs["DRAW"]])

	def init_cameras(self):
		screen_size = self.get_size()
		self.game_camera = Camera(constants.VIRTUAL_SIZE)
		self.game_camera.set_size(Vector(screen_size[0], screen_size[1]))

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