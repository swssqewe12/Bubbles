from ICController import *
from InputControl import *
from pyglet.window import key
import btn

# Connect profiles

def keyboard_player_connect(icc, ic_connect):
	icc.add_key_control(key.A, ic_connect, 1)

def xbox_player_connect(icc, ic_connect):
	icc.add_joy_btn_control(btn.xbox.A, ic_connect, 1)

# Player profiles

def keyboard_player_controller(icc, ic_x, ic_y, ic_sprint, ic_dash):
	icc.add_key_control(key.APOSTROPHE,	ic_x,		 1)
	icc.add_key_control(key.L,			ic_x,		-1)
	icc.add_key_control(key.P,			ic_y,		 1)
	icc.add_key_control(key.SEMICOLON,	ic_y,		-1)
	icc.add_key_control(key.LSHIFT,		ic_sprint,	 1)
	icc.add_key_control(key.D,			ic_dash,	 1)

def xbox_player_controller(icc, ic_x, ic_y, ic_sprint, ic_dash):
	icc.add_joy_motion_control('x', ic_x, (-1,  1), min=0.2)
	icc.add_joy_motion_control('y', ic_y, ( 1, -1), min=0.2)
	icc.add_joy_btn_control(btn.xbox.X,  ic_dash,	1)
	icc.add_joy_btn_control(btn.xbox.L3, ic_sprint,	1)

# ICController builders

def build_player_connect_icc(profile):
	icc = ICController()
	ic_connect = InputControl()
	profile(icc, ic_connect)
	return icc, ic_connect

def build_player_controller_icc(profile):
	icc = ICController()
	ic_x		= InputControl()
	ic_y		= InputControl()
	ic_sprint	= InputControl()
	ic_dash		= InputControl()
	profile(icc, ic_x, ic_y, ic_sprint, ic_dash)
	return icc, ic_x, ic_y, ic_sprint, ic_dash