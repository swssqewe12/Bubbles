class PygletICCBinder:
	
	def __init__(self, icc):
		self.icc = icc

	def on_key_press(self, symbol, modifiers):
		self.icc.on_key_down(symbol, modifiers)

	def on_key_release(self, symbol, modifiers):
		self.icc.on_key_up(symbol, modifiers)
	
	def on_joybutton_press(self, joystick, button):
		self.icc.on_joy_btn_down(button)

	def on_joybutton_release(self, joystick, button):
		self.icc.on_joy_btn_up(button)

	def on_joyaxis_motion(self, joystick, axis, value):
		self.icc.on_joy_motion(axis, value)