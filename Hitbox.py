class Hitbox:
	def __init__(self, collider, attack_dir, fixed_force=0, variable_force=0, damage=0, movement_stun_time=0):
		self.collider = collider
		self.fixed_force = fixed_force
		self.variable_force = variable_force
		self.damage = damage
		self.attack_dir = attack_dir
		self.movement_stun_time = movement_stun_time
		self.hit_entities = {}