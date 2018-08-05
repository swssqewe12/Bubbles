import math
TWO_PI = math.pi * 2

def normalized_rot(rot):
	return rot % TWO_PI

def rot_diff(a, b):
	diff = normalized_rot(a) - normalized_rot(b)
	if   diff < -math.pi: diff += TWO_PI
	elif diff >  math.pi: diff -= TWO_PI
	return diff