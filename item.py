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
		self.items = []
		self.app = app

	def shop(self, playerobj):
		self.app.write("Welcome to the Shop!")
		self.app.write("")
		time.sleep(1)
		while True:
			self.app.write("Select player:")
			for i, player in enumerate(playerobj.players):
				self.app.write("	{}. {}".format(i, player))
			self.app.write("	e. exit ~ Warning ~ This will delete the shop for good")
			self.app.wait_variable(self.app.inputVariable)
			ans = self.app.inputVariable.get()


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
