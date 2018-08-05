class ICController:
	def __init__(self):
		self.key_controls = {}
	
	def on_key_down(self, symbol, modifiers):
		controls = self.key_controls.get(symbol, [])
		for ic, change in controls:
			ic.add_amt(change)

	def on_key_up(self, symbol, modifiers):
		controls = self.key_controls.get(symbol, [])
		for ic, change in controls:
			ic.add_amt(-change)

	def add_key_control(self, key, ic, change=1):
		controls = self.key_controls.get(key, None)
		if not controls:
			controls = []
			self.key_controls[key] = controls
		controls.append((ic, change))