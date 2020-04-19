from BubbleSprite import *
from CircleCollider import *
from Hurtbox import *
from Sprite import *
from Vector import *

# Components
from AttackBoxes import *
from BoostControl import *
from Bubble import *
from Collidable import *
from Damage import *
from DashControl import *
from DodgeControl import *
from Motion import *
from MovementControl import *
from Particles import *
from PlayerTag import *
from Renderable import *
from Stunnable import *
from Trail import *
from Transform import *

from Cleanup import *

class EntityFactory:
	@staticmethod
	def create_player(world, camera, ic_x, ic_y, ic_sprint, ic_dash):

		# Shared data
		spr_head = Sprite("head")

		# Components
		transform = Transform()
		bcontrol = BoostControl(ic_dash)
		dcontrol = DashControl(ic_dash)

		rend = Renderable()
		head = rend.add_sprite(spr_head)
		rend.camera = camera

		mcontrol = MovementControl()
		mcontrol.add_dir_control(ic_x, Vector(1, 0))
		mcontrol.add_dir_control(ic_y, Vector(0, 1))
		mcontrol.ic_sprint = ic_sprint
		
		bubble = Bubble()
		bubble.camera = camera
		bubble.add_bubble_sprite(BubbleSprite("head", 2, sbo=64 + 63,
			scale_func	 = lambda x,y: spr_head.transform.scale,
			opacity_func = lambda x,y: spr_head.opacity))
		bubble.add_bubble_sprite(BubbleSprite("offscreen_bubble", 1, sbo=112.5,
			scale_func	 = lambda x,y: spr_head.transform.scale,
			opacity_func = lambda x,y: 0.8,
			rot_func	 = lambda bub_spr,_: mathutils.DEG_180-Vector(bub_spr.offscreen_x, bub_spr.offscreen_y).to_rot()+mathutils.DEG_90))
		bubble.roo = 64

		attack_boxes = AttackBoxes()
		attack_boxes.hurtboxes.append(Hurtbox(CircleCollider(Vector(0, 0), 64, rel_pos=lambda pos: transform.pos.added_to(pos))))
		
		collidable = Collidable([CircleCollider(Vector(0, 0), 64, rel_pos=lambda pos: transform.pos.added_to(pos))])
		collidable.bounce = 0.1

		return world.create_entity(transform, rend, mcontrol, bcontrol, dcontrol, bubble, attack_boxes, collidable,
			Trail(), PlayerTag(), Motion(), Trail(), Particles(), Damage(), Stunnable())

	@staticmethod
	def destroy_entity(world, ent):
		world.add_component(ent, Cleanup())