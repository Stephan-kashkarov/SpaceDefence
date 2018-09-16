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
	def __init__(self, x, y, app):
		self.x = x
		self.y = y
		self.items = self.randomItems()
		self.app = app

	def shop(self, playerobj):
		self.app.write("Welcome to the Shop!")
		self.app.write("")
		time.sleep(1)
		while True:
			self.app.write("Select player:")
			for i, player in enumerate(playerobj.players):
				self.app.write("	{}. {} (Funds: ${})".format(i, player, player.money))
			self.app.write("	e. exit")
			self.app.wait_variable(self.app.inputVariable)
			ans = self.app.inputVariable.get()
			player = playerobj.players[ans]
			self.app.write("Player Selected: {} the {}".format(player.name, player.__class__.__name__))
			self.app.write("")
			while True:
				self.app.write("Select an Item:")
				for i, item in enumerate(self.items):
					self.app.write("	{}. {} ( ${} )".format(i, item, item.cost))
				self.app.write("	b. Back")
				self.app.write("	e. exit")
				try:
					self.app.wait_variable(self.app.inputVariable)
					ans = self.app.inputVariable.get()
					if ans == "b":
						break
					elif ans == "e":
						return None

					if ans not in range(len(self.items)):
						raise ValueError
					item = self.items.pop(i)
					if item.cost > player.money:
						self.items.append(item)
						raise ValueError
					player.money -= item.cost
					player.items.append(item)
				except ValueError:
					self.app.write("Item too expensive / invalid choice")

	def randomItems(self):
		items = []
		items.append(Health_shot())
		items.append(Adernaline_shot())
		items.append(Medkit())
		if random.randint(0, 1) == 1:
			items.append(Vest())
		else:
			items.append(Tinfoil_hat)

		if random.randint(0, 10) == 7:
			items.append(Explosive_ammo)
		elif random.randint(0,15) == 7:
			items.append(Armour)
		return items


class Item(object):
	def __init__(self):
		self.name = ""
		self.ammount = 1
		self.max_health = 0
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
			player.max_health += self.max_health
			player.health += self.health
			player.attack += self.attack
			player.defense += self.defense
			player.mind += self.mind
			player.resistance += self.resistance
			player.adrenaline += self.adrenaline
			return True
		else:
			return False


class Health_shot(Item):
	def __init__(self):
		super().__init__()
		self.name = "Health Shot"
		self.health = 10
		self.adrenaline = 5
		self.cost = 10


class Adernaline_shot(Item):
	def __init__(self):
		super().__init__()
		self.name = "Adernaline Shot"
		self.adrenaline = 25
		self.health = -10
		self.cost = 10


class Medkit(Item):
	def __init__(self):
		super().__init__()
		self.name = "Medkit"
		self.health = 40
		self.adrenaline = 2
		self.cost = 30


class Vest(Item):
	def __init__(self):
		super().__init__()
		self.name = "Vest"
		self.defense = 25
		self.cost = 30


class Tinfoil_hat(Item):
	def __init__(self):
		super().__init__()
		self.name = "Tinfoil Hat"
		self.resistance = 4
		self.defense = -2
		self.cost = 40



class Explosive_ammo(Item):
	def __init__(self):
		super().__init__()
		self.name = "Explosive Ammo"
		self.attack = 10
		self.cost = 100


class Armour(Item):
	def __init__(self):
		super().__init__()
		self.name = "Armour"
		self.max_health = 50
		self.cost = 120
