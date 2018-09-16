#!/bin/python3.6
"""
rpg.py - entry point for the RPG Game

Written by Stephan Kashkarov 
for Intermediate Programming
Python RPG Assignment 2018
"""

import time
import random

class Shop(object):
	"""Shop object"""
	def __init__(self, x, y, app):
		"""Initializes shop object with rand items"""
		self.x = x
		self.y = y
		self.items = self.randomItems()
		self.app = app

	def shop(self, playerobj):
		"""Shop interface for party"""
		self.app.write("Welcome to the Shop!")
		self.app.write("")
		time.sleep(1)

		while True:
			self.app.write("Select player:")
			for i, player in enumerate(playerobj.players):
				self.app.write("	{}. {} (Funds: ${})".format(i, player.name, player.money))
			self.app.write("	e. exit") # exit store
			self.app.write("")
			self.app.wait_variable(self.app.inputVariable)
			ans = self.app.inputVariable.get()

			player = playerobj.players[int(ans)] # selects player
			self.app.write("Player Selected: {} the {}".format(player.name, player.__class__.__name__))
			self.app.write("")
			while True:
				self.app.write("Select an Item:") # selects items
				for i, item in enumerate(self.items):
					self.app.write("	{}. {} ( ${} )".format(i, item.name, item.cost))
				self.app.write("	b. Back") # choose different char
				self.app.write("	e. exit") # exits store
				try:
					# get input
					self.app.wait_variable(self.app.inputVariable)
					ans = self.app.inputVariable.get()
					if ans == "b":
						break
					elif ans == "e":
						return None

					if int(ans) not in range(len(self.items)): # if ans not valid
						raise ValueError
					item = self.items.pop(int(ans)) # pops item from store
					if item.cost > player.money: # if item too expessive
						self.items.append(item) # puts item back into store
						raise ValueError
					player.money -= item.cost # removes cost
					player.inventory.append(item) # appends item to inventory
				except ValueError:
					self.app.write("Item too expensive / invalid choice")

	def randomItems(self):
		"""Randomises items in store"""
		items = []
		items.append(Health_shot())
		items.append(Adernaline_shot())
		items.append(Medkit())
		if random.randint(0, 1) == 1: # 50% chance of item
			items.append(Vest())
		else:
			items.append(Tinfoil_hat())

		if random.randint(0, 10) == 7: # 10% chance of item
			items.append(Explosive_ammo)
		elif random.randint(0,15) == 7: # 1/15% chance of item
			items.append(Armour)
		return items


class Item(object):
	"""Base item object for inventory system"""
	def __init__(self):
		"""Initialises item object"""
		self.name = ""
		self.ammount = 1
		self.max_health = 0
		self.health = 0
		self.attack = 0
		self.defense = 0
		self.resistance = 0
		self.adrenaline = 0
		self.cost = 0

	def use(self, player):
		"""Uses seleced item on defined player"""
		if self.ammount > 0:
			self.ammount -= 1
			player.max_health += self.max_health
			player.health += self.health
			player.attack += self.attack
			player.defense += self.defense
			player.mind += self.mind
			player.resistance += self.resistance
			player.adrenaline += self.adrenaline
			return True # it worked
		else:
			return False # it didnt


class Health_shot(Item):
	"""Item Health shot subclass of item """
	def __init__(self):
		""" initialises item Health shot"""
		super().__init__() # inits item class
		self.name = "Health Shot"
		self.health = 10
		self.adrenaline = 5
		self.cost = 10


class Adernaline_shot(Item):
	"""Item Adrenaline shot subclass of item """
	def __init__(self):
		""" initialises item Adrenaline shot"""
		super().__init__()
		self.name = "Adernaline Shot"
		self.adrenaline = 25
		self.health = -10
		self.cost = 10


class Medkit(Item):
	"""Item Medkit subclass of item """
	def __init__(self):
		""" initialises item Medkit"""
		super().__init__()
		self.name = "Medkit"
		self.health = 40
		self.adrenaline = 2
		self.cost = 30


class Vest(Item):
	"""Item Vest subclass of item """
	def __init__(self):
		""" initialises item Vest"""
		super().__init__()
		self.name = "Vest"
		self.defense = 25
		self.cost = 30


class Tinfoil_hat(Item):
	"""Item Tinfoil hat subclass of item """
	def __init__(self):
		""" initialises item Tinfoil hat"""
		super().__init__()
		self.name = "Tinfoil Hat"
		self.resistance = 4
		self.defense = -2
		self.cost = 40


class Explosive_ammo(Item):
	"""Item Exposive ammo subclass of item """
	def __init__(self):
		""" initialises item Exposive ammo"""
		super().__init__()
		self.name = "Explosive Ammo"
		self.attack = 10
		self.cost = 100


class Armour(Item):
	"""Item Armour subclass of item """
	def __init__(self):
		""" initialises item Armour"""
		super().__init__()
		self.name = "Armour"
		self.max_health = 50
		self.cost = 120
