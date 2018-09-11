#!/usr/local/bin/python3.6
"""
rpg.py - entry point for the RPG Game

Written by Stephan Kashkarov 
for Intermediate Programming
Python RPG Assignment 2018
"""

import math
import character
import random
from pprint import pprint


def make_map(x, y, val, boundry=False):
	map = []
	if boundry:
		map.append([])
		for j in range(y + 1):
			map[0].append("#")
	for i in range(1, x):
		if boundry:
			map.append(["#"])
		for j in range(1, y):
			map[i].append(val)
		if boundry:
			map[i].append("#")
	if boundry:
		map.append([])
		for j in range(y + 1):
			map[-1].append("#")
	return map


class Map(object):

	def __init__(self, players, size, mode, difficulty, app):
		self.player = Player_group(0, 0, players)
		self.x = size
		self.y = size
		self.difficulty = difficulty
		self.enemies = self.generate_enemies(int(size/8), mode)
		self.app = app
		self.map = make_map(size, size, " ", True)
		

		# self.map = Generator(128, 10)
		# self.map.generate()

	def generate_enemies(self, num, team):
		names = {
			2: [
				"Floater",
				"Sectoid",
				"Muton",
				"Etheral"
			],
			1: [
				"Jensen",
				"Marsh",
				"Greenwood",
				"Bear",
				"Eagle",
				"Jock",
				"Maximus",
				"Pheonix",
				"Jackson",
				"Fox",
				"Cheetah"
			]
		}
		enemies = []
		for i in range(num):
			group = []
			if team == 1:
				if self.difficulty == "e":
					if random.randint(0, 3) == 1:
						size = 3
					else:
						size = 4
					for i in range(size):
						group.append(character.Floater(names[2][0], self.app))
				elif self.difficulty == "m":
					size = 4
					for i in range(size):
						if random.randint(0, 1) == 1:
							if random.randint(0, 3) == 3:
								group.append(character.Muton(names[2][2], self.app))
							else:
								group.append(character.Sectoid(names[2][1], self.app))
						else:
							group.append(character.Floater(names[2][0], self.app))
				elif self.difficulty == "h":
					if random.randint(0, 3) == 1:
						size = 4
					else:
						size = 5
					for i in range(size):
						if random.randint(0, 1) == 1:
							if random.randint(0, 10) == 10:
								group.append(character.Ethereal(names[2][3], self.app))
							else:
								group.append(character.Muton(names[2][2], self.app))
						else:
							group.append(character.Sectoid(names[2][1], self.app))
				else:
					if random.randint(0, 10) == 10:
						size = 6
					else:
						size = 5
					for i in range(size):
						if random.randint(0, 1) == 1:
							if random.randint(0, 3) == 3:
								group.append(character.Ethereal(names[2][3], self.app))
							else:
								group.append(character.Muton(names[2][2], self.app))
						else:
							group.append(character.Sectoid(names[2][1], self.app))

			# TODO make decisions for human AI
			if team == 2:
				if self.difficulty == "e":
					size = 2
				elif self.difficulty == "m":
					size = 3
				elif self.difficulty == "h":
					size = 3
				else:
					size = 4
			enemies.append(group)
		return enemies

	def draw(self):
		self.app.write("X"*33)
		for y in range(self.player.y - 16, self.player.y + 16):
			if y >= len(self.map) or y < 0:
				row = "X" + "."*31 + "X"
				continue
			for x in range(self.player.x - 16, self.player.x + 16):
				if y >= len(self.map) or y < 0:
					row += "."
					continue
				row += self.map[y][x]
			self.app.write(row)
		self.app.write("X"*33)

	def check(self, y, x, obj):
		x1 = obj.x
		y1 = obj.y
		try:
			if self.map[y1 + y][x1 + x] == " ":
				self.map[y1][x1] = " "
				if obj.__class__.__name__ != "Ai_group":
					self.map[y1 + y][x1 + x] = "X"
				else:
					self.map[y1 + y][x1 + x] = "E"
				obj.x += x
				obj.y += y
				return True
			elif obj.__class__.__name__ != "Ai_group":
				if self.map[y1 + y][x1 + x] == "$":
					obj.x += x
					obj.y += y
					return 'shop'
				elif self.map[y1 + y][x1 + x] == "E":
					obj.x += x
					obj.y += y
					return 'battle'
				else:
					return False
			elif obj.__class__.__name__ == "Ai_group":
				if self.map[y1 + y][x1 + x] == 'X':
					obj.x += x
					obj.y += y
					return 'battle'
				else:
					return False
		except IndexError:
			return False

	def run(self):
		while True:
			situation, player, leave = self.player_move()
			if situation == 'battle':
				return player, False
			if situation == 'shop':
				player.run(player)
			enemies = self.ai_move()
			if enemies:
				return enemies, False
	def player_move(self):
		while True:
			self.draw()
			self.app.write("Choose a direction to move! (wasd or hjkl(vim style))")
			self.app.write("Press 0 to pass your move")
			self.app.write("")
			self.app.wait_variable(self.app.inputVariable)
			move = self.app.inputVariable.get()
			try:
				if move == '0':
					pass
				elif move == "quit":
					self.app.quit()
				elif move == "w" or move == "j":
					move = self.check(-1, 0, self.player)
					break
				elif move == "s" or move == "k":
					move = self.check(1, 0, self.player)
					break
				elif move == "a" or move == "h":
					move = self.check(0, -1, self.player)
					break
				elif move == "d" or move == "l":
					move = self.check(0, 1, self.player)
					break
				else:
					raise ValueError
				if move == 'battle':
					for enemy in self.enemies:
						if enemy.x == self.player.x and enemy.y == self.player.y:
							return 'battle', enemy.enemies, False
			except ValueError:
				self.app.write("Invalid Input")

	def ai_move(self):
		for group in self.enemies:
			move = False
			while not move:
				if abs(self.player.x - group.x) < 16:
					pass # * move towards player
				else:
					x_change = random.randint(-1, 1)
					y_change = random.randint(-1, 1)
				move = self.check(y_change, x_change, group)
				if move == 'battle':
					return self.enemies.enemies, False



class Ai_group(object):
	def __init__(self, x, y, enemies):
		self.x = x
		self.y = y
		self.enemies = enemies

class Player_group(object):
	def __init__(self, x, y, players):
		self.x = x
		self.y = y
		self.group_inventory = []
		self.players = players



class Room(object):
	"""Room Object ~
		Keeps data for a single room in the
		map with data such as size and type
	"""
	def __init__(self, x1, y1, x2, y2, base):
		"""initialiser for Room Object"""
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.repr = base

	def create(self):
		""" Create Method ~
		draws the object onto a blank map
		for merger process
		"""
		for j in range(int(self.x1), int(self.x2)):
				for k in range(self.y1, self.y2):
					self.repr[j][k] = 1

		return self.repr

	def checkOverlap(self, room):
		"""Check overlap Method ~
		this method takes in another room object and returns if the two rooms
		are overlapping or not. This method is used in Map object's moveBoxes method
		"""
		if (int(room.x1) in range(int(self.x1), int(self.x2)) or int(room.x2) in range(int(self.x1), int(self.x2)))\
		and(int(room.y1) in range(int(self.y1), int(self.y2)) or int(room.y2) in range(int(self.y1), int(self.y2))):
			return True
		else:
			return False


class Generator(object):
	"""Generator object ~ 
		This object generates the map and keeps track of its current situation 
	"""

	def __init__(self, size=255, rooms=10):
		"""Initialiser for Map"""
		self.x = size if size > 128 else 128
		self.y = size if size > 128 else 128
		self.rooms = rooms
		self.map = make_map(self.x, self.y, 0)
		self.roomlst = []


	def randomPoint(self):
		"""random Point Method ~
		Selects a random point within defined space
		"""
		# mid rect width, height 20%
		x = random.randint(abs((self.x / 2) - self.x / 8),
						   abs((self.x / 2) + self.x / 8))
		y = random.randint(abs((self.y / 2) - self.y / 8),
						   abs((self.y / 2) + self.y / 8))
		return x, y


	def generate(self):
		"""generate Method ~
		Contains the correct order of calls for a map to be generated.
		 -> Called in the initaliser
		"""
		self.createBoxes()
		self.moveBoxes()


	def createBoxes(self):
		""" Create Boxes method
		This method creates a bunch of boxes in a small space on
		the map. This allows for the initial generation of the
		rooms on the map before the moveBoxes method is called.
		"""
		for i in range(self.rooms):
			x1, y1 = self.randomPoint()
			x2, y2 = self.randomPoint()
			a = Room(x1, y1, x2, y2, self.map)
			self.roomlst.append(a)


	def moveBoxes(self):
		""" Move Boxes Method ~
		This method is used to separate all the overlapping boxes
		created by the Create boxes method. This it to allow for
		the rooms to finalise their position in the maze before
		the rooms are purged.
		"""
		moving = True
		exits = []
		while moving: # while moving boxes
			for i, room in enumerate(self.roomlst): # grab each room and index
				print("First | i: {}, room: {}". format(i, room))
				for roomIndex in range(0, i): # loop through every room below current
					room2 = self.roomlst[roomIndex] # shortens handle
					x = room.x1 - room2.x1 # detects run
					y = room.y1 - room2.y1 # detects rise
					overlap = room.checkOverlap(room2)
					while overlap: # while the roomlst are still overlapping
						print("x1: {}, x2: {}, y1: {}, y2: {} | Overlap: {}".format(
							room.x1, room.x2, room.y1, room.y2, overlap
							)
						)
						room.x1 += math.sin(x) # sinwave move
						room.x2 += math.sin(x) # sinwave move
						room.y1 += math.sin(y) # sinwave move
						room.y2 += math.sin(y) # sinwave move
						overlap = room.checkOverlap(room2)
			exits = []
			for i, room in enumerate(self.roomlst): # grab each room and index
				for roomIndex in range(i, len(self.rooms)): # loop through all rooms after current
					if room.checkOverlap(self.rooms[roomIndex]): # if they overlap
						exits.append(True)
						break # start again
					else:
						exits.append(False)
				print("Exit Status: {}, Len of Exits: {}/{}".format(True in exits, len(exits), len(self.rooms)**2))
		if True in exits:
			break
	if True not in exits:
		break
print("Bad")