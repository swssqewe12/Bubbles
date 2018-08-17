class Collider:
	def check(self, other, collision_info=None):
		return getattr(self, "check_" + other.__class__.__name__, Collider.FALSE_FUNC)(other, collision_info)

	FALSE_FUNC = lambda *args, **kwargs: False