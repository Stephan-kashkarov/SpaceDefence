"""rpg.py - entry point for the RPG Game
   Written by Stephan Kashkarov 
   for Intermediate Programming
   Python RPG Assignment 2018
"""

class Item(object):
	def __init__(self):
		self.ammount = 1
		self.health = 0
		self.attack = 0
		self.defense = 0
		self.mind = 0
		self.resistance = 0
		self.adrenaline = 0
		self.cost = 0

	def use(self, player):
		if self.ammount > 0:
			self.ammount -= 1
			player.health += self.health
			player.attack += self.attack
			player.defense += self.defense
			player.mind += self.mind
			player.resistance += self.resistance
			player.adrenaline += self.adrenaline
			return True

		else:
			return False


class Adernaline_shot(Item):
	def __init__(self, ):
		super().__init__()
		self.name = "Adernaline Shot"
		self.adrenaline = 25
		self.health = -10
		self.cost = 10
