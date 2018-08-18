import math
HALF_PI	= math.pi / 2
PI = math.pi
TWO_PI = math.pi * 2

DEG_15	= HALF_PI / 6
DEG_45	= HALF_PI / 2
DEG_90	= HALF_PI
DEG_135	= 3 * math.pi / 4
DEG_180	= PI

DEG_NEG_15	= -DEG_15
DEG_NEG_45	= -DEG_45
DEG_NEG_90	= -DEG_90
DEG_NEG_135	= -DEG_135
DEG_NEG_180	= -DEG_180

def normalized_rot(rot):
	return rot % TWO_PI

def rot_diff(a, b):
	diff = normalized_rot(a) - normalized_rot(b)
	if   diff < -math.pi: diff += TWO_PI
	elif diff >  math.pi: diff -= TWO_PI
	return diff

def map_range(x, a, b, c, d):
   return (x-a)/(b-a)*(d-c)+c