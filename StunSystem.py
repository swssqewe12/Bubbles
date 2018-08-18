import esp

# Components
from Stunnable import *
from MovementControl import *
from BoostControl import *
from DashControl import *
from DodgeControl import *

class StunSystem(esp.Processor):

	def update(self, dt):
		for ent, stunnable in self.world.get_component(Stunnable):
			amt = 0
			if stunnable.stun_time_left > 0:
				stunnable.stun_time_left = max(stunnable.stun_time_left - dt, 0)
				if stunnable.stun_time_left == 0: amt = -1
			if stunnable.prepare_stun:
				stunnable.prepare_stun = False
				amt = 1
			if amt != 0:
				mcontrol = self.world.get_entity_component(ent, MovementControl)
				if mcontrol: mcontrol.disabled += amt
				bcontrol = self.world.get_entity_component(ent, BoostControl)
				if bcontrol: bcontrol.disabled += amt
				dcontrol = self.world.get_entity_component(ent, DashControl)
				if dcontrol: dcontrol.disabled += amt
				dcontrol = self.world.get_entity_component(ent, DodgeControl)
				if dcontrol: dcontrol.disabled += amt