import mathutils

class ICController:
	def __init__(self):
		self.key_controls = {}
		self.joy_btn_controls = {}
		self.joy_motion_controls = {}
	
	def on_key_down(self, symbol, modifiers):
		controls = self.key_controls.get(symbol, [])
		for ic, change in controls:
			ic.add_amt(change)

	def on_key_up(self, symbol, modifiers):
		controls = self.key_controls.get(symbol, [])
		for ic, change in controls:
			ic.add_amt(-change)

	def on_joy_btn_down(self, symbol):
		controls = self.joy_btn_controls.get(symbol, [])
		for ic, change in controls:
			ic.add_amt(change)

	def on_joy_btn_up(self, symbol):
		controls = self.joy_btn_controls.get(symbol, [])
		for ic, change in controls:
			ic.add_amt(-change)

	def on_joy_motion(self, axis, value):
		controls = self.joy_motion_controls.get(axis, [])
		for ic, range, min in controls:
			value = mathutils.map_range(value, -1, 1, range[0], range[1])
			if abs(value) < min: value = 0
			ic.set_amt(value)

	def add_key_control(self, key, ic, change=1):
		controls = self.key_controls.get(key, None)
		if not controls:
			controls = []
			self.key_controls[key] = controls
		controls.append((ic, change))

	def add_joy_btn_control(self, btn, ic, change=1):
		controls = self.joy_btn_controls.get(btn, None)
		if not controls:
			controls = []
			self.joy_btn_controls[btn] = controls
		controls.append((ic, change))

	def add_joy_motion_control(self, axis, ic, range=(-1, 1), min=0):
		controls = self.joy_motion_controls.get(axis, None)
		if not controls:
			controls = []
			self.joy_motion_controls[axis] = controls
		controls.append((ic, range, min))