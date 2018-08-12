import os, pyglet
import constants

ANCHOR_MODE_POSITION = 0
ANCHOR_MODE_CENTER = 1

def load_image(path, anchor_x=0, anchor_y=0, anchor_mode=ANCHOR_MODE_POSITION):
	image = pyglet.image.load(os.path.join(constants.ROOT_DIR, path))
	if anchor_mode == ANCHOR_MODE_POSITION:
		image.anchor_x = anchor_x
		image.anchor_y = anchor_y
	elif anchor_mode == ANCHOR_MODE_CENTER:
		image.anchor_x = int(image.width / 2)
		image.anchor_y = int(image.height / 2)
	return image

images = {
	"head": load_image("res/img/characters/normal/green/head.png", anchor_mode=ANCHOR_MODE_CENTER),
	"tail": load_image("res/img/characters/normal/green/tail.png", anchor_mode=ANCHOR_MODE_CENTER),
	"dashcloud": load_image("res/img/dashcloud.png", anchor_mode=ANCHOR_MODE_CENTER),
}