class Hitbox:
	def __init__(self, collider, attack_dir, fixed_force=0, variable_force=0, damage=0, stun_time=0, onhit=None):
		self.collider = collider
		self.fixed_force = fixed_force
		self.variable_force = variable_force
		self.damage = damage
		self.attack_dir = attack_dir
		self.stun_time = stun_time
		self.hit_entities = {}
		self.onhit = None