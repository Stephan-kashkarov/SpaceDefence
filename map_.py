#!/usr/local/bin/python3.6
"""
rpg.py - entry point for the RPG Game

Written by Stephan Kashkarov 
for Intermediate Programming
Python RPG Assignment 2018
"""

import math
import random

# from numpy import array
# from scipy.spatial import Delaunay
# from scipy.sparse import csr_matrix
# from scipy.sparse.csgraph import minimum_spanning_tree

import character
import item


def make_map(x, y, val, boundry=False):
	"""Empty map generator function"""
	map = []
	if boundry: # makes boundries
		map.append([])
		for j in range(y + 1):
			map[0].append("#")
	for i in range(1 if boundry else 0, x):
		if boundry:
			map.append(["#"])
			for j in range(1, y):
				map[i].append(val) # appends local val
			map[i].append("#")
		else:
			map.append([])
			for j in range(y):
				map[i].append(val)
	if boundry:
		map.append([])
		for j in range(y + 1):
			map[-1].append("#")
	return map # returns


class Map(object): # map object

	def __init__(self, players, mode, difficulty, app):
		"""Initialises the map object and generates map and spawns"""
		self.app = app
		self.difficulty = difficulty
		# selects size based on difficulty
		if self.difficulty == "e":
			size = 8
		elif self.difficulty == "m":
			size = 16
		elif self.difficulty == "h":
			size = 32
		elif self.difficulty == "l":
			size = 64
		else:
			size = random.randint(8, 64)
		self.map = make_map(size, size, " ", True) # makes a map
		self.x = size
		self.y = size
		self.generate_obsticles() # gens obsticles
		self.player = self.generate_player(players) # gens player
		self.enemies = self.generate_enemies(int(size/8), mode) # gens enemies
		self.shops = self.generate_shops(int(size/16)) # gens shops
		

		# self.map = Generator(128, 10)
		# self.map.generate()

	def generate_obsticles(self):
		"""Generates obsticles for map"""
		for i in range(int(self.x/2)):
			while True:
				# brute forces empty time
				x = random.randint(1, len(self.map) - 1)
				y = random.randint(1, len(self.map) - 1)
				if self.map[y][x] == " ":
					break
			shape = random.randint(0, 2) # choses shape
			if shape == 0: # if box
				for i in range(y, y + int(self.y/8)):
					for j in range(x, x + int(self.x/8)):
						try:
							if self.map[i][j] != "#":
								self.map[i][j] = "O"
						except:
							pass
			elif shape == 1: # if ver line
				for i in range(y, y + int(self.y/4)):
					try:
						if self.map[i][x] != "#":
							self.map[i][x] = "O"
					except:
						pass
			else: # if hoz line
				for i in range(x, x + int(self.x/4)):
					try:
						if self.map[y][i] != "#":
							self.map[y][i] = "O"
					except:
						pass

	def generate_player(self, players):
		"""Generates player object"""
		while True:
			# brute forces it
			x = random.randint(0, self.x)
			y = random.randint(0, self.y)
			if self.map[y][x] == " ":
				self.map[y][x] = "X"
				return Player_group(x, y, players)

	def generate_shops(self, num):
		"""Generates shop objects"""
		shops = []
		# brute forces it num times
		for i in range(num):
			while True:
				x = random.randint(0, self.x)
				y = random.randint(0, self.y)
				if self.map[y][x] == " ":
					self.map[y][x] = "$"
					shops.append(item.Shop(x, y, self.app))
					break

		return shops

	def generate_enemies(self, num, team):
		# local vars
		names = {
			2: [
				"Floater",
				"Sectoid",
				"Muton",
				"Etheral",
				"Queen"
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
			# makes battle group by difficuly
			group = []
			if team == 1:
				if self.difficulty == 'r':
					difficulty = random.randint(0, 3) # randomies difficulty of random eney type
				else:
					if self.difficulty == 'e':
						difficulty = 0
					elif self.difficulty == 'm':
						difficulty = 1
					elif self.difficulty == 'h':
						difficulty = 2
				if difficulty == 0: # easy difficutly
					# chooses battle group size
					if random.randint(0, 3) == 1:
						size = 3
					else:
						size = 4
					for i in range(size):
						# chooses enemies
						group.append(character.Floater(names[2][0], self.app))
				elif difficulty == 1:
					# chooses battle group size
					size = 4
					for i in range(size):
						if random.randint(0, 1) == 1:
							if random.randint(0, 3) == 3:
								group.append(character.Muton(names[2][2], self.app))
							else:
								group.append(character.Sectoid(names[2][1], self.app))
						else:
							group.append(character.Floater(names[2][0], self.app))
				elif difficulty == 2:
					# chooses battle group size
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
				elif difficulty == 3:
					# chooses battle group size
					if random.randint(0, 10) == 10:
						size = 6
					else:
						size = 5
					for i in range(size):
						if random.randint(0, 1) == 1:
							if random.randint(0, 3) == 3:
								group.append(character.Queen(names[2][4], self.app))
							else:
								group.append(character.Muton(names[2][2], self.app))
						else:
							group.append(character.Sectoid(names[2][1], self.app))

			if team == 2:
				if self.difficulty == 'r':
					difficulty = random.randint(0, 3)
				else:
					if self.difficulty == 'e':
						difficulty = 0
					elif self.difficulty == 'm':
						difficulty = 1
					elif self.difficulty == 'h':
						difficulty = 2

				if difficulty == 0:
					# chooses battle group size
					if random.randint(0, 3) == 1:
						size = 2
					else:
						size = 3
					for i in range(size):
						rand_name = names[1][random.randint(0, len(names[1]) - 1)]
						group.append(character.Assault(rand_name, self.app))
				elif difficulty == 1:
					# chooses battle group size
					size = 3
					for i in range(size):
						rand_name = names[1][random.randint(0, len(names[1]) - 1)]
						if random.randint(0, 1) == 1:
							if random.randint(0, 3) == 3:
								group.append(character.Heavy(rand_name, self.app))
							else:
								group.append(character.Sniper(rand_name, self.app))
						else:
							group.append(character.Assault(rand_name, self.app))
				elif difficulty == 2:
					# chooses battle group size
					if random.randint(0, 3) == 1:
						size = 3
					else:
						size = 4
					for i in range(size):
						rand_name = names[1][random.randint(0, len(names[1]) - 1)]
						if random.randint(0, 1) == 1:
							if random.randint(0, 10) == 10:
								group.append(character.Ethereal(rand_name, self.app))
							else:
								group.append(character.Heavy(rand_name, self.app))
						else:
							group.append(character.Sniper(rand_name, self.app))
				else:
					# chooses battle group size
					if random.randint(0, 10) == 10:
						size = 5
					else:
						size = 4
					for i in range(size):
						rand_name = names[1][random.randint(0, len(names[1]) - 1)]
						if random.randint(0, 1) == 1:
							if random.randint(0, 3) == 3:
								group.append(character.Support(rand_name, self.app))
							else:
								group.append(character.Heavy(rand_name, self.app))
						else:
							group.append(character.Sniper(rand_name, self.app))

			# brute forces a location for group
			while True:
				x = random.randint(1, len(self.map) - 1)
				y = random.randint(1, len(self.map) - 1)
				if self.map[y][x] == " ":
					break
			# instacniates a class
			group = Ai_group(x, y, group)
			enemies.append(group)
		return enemies

	def draw(self):
		"""Draws the map object"""
		self.app.write("X"*66) # top row
		for y in range(self.player.y - 16, self.player.y + 16): # 16 either side
			row = "X"
			if y >= len(self.map) or y < 0:
				row = "X" + "."*64  # out of range
			else:
				for x in range(self.player.x - 32, self.player.x + 32): # 32 either side
					if x >= len(self.map) or x < 0:
						row += "." # out of range
						continue
					row += self.map[y][x]
			row += "X"
			self.app.write(row) # draws row
		self.app.write("X"*66) # bottom row

	def check(self, y, x, obj):
		"""Validates move for object by x and y"""
		# makes local vars
		x1 = obj.x
		y1 = obj.y
		try:
			# if empty square just move and update your char location
			if self.map[y1 + y][x1 + x] == " " or self.map[y1 + y][x1 + x] == "," or self.map[y1 + y][x1 + x] == "*":
				self.map[y1][x1] = " "
				if obj.__class__.__name__ != "Ai_group":
					self.map[y1][x1] = "*"
					self.map[y1 + y][x1 + x] = "X"
				else:
					self.map[y1][x1] = ","
					self.map[y1 + y][x1 + x] = "E"
				obj.x += x
				obj.y += y
				return True
			# if obj is not Ai
			elif obj.__class__.__name__ != "Ai_group":
				if self.map[y1 + y][x1 + x] == "$": # go through shop
					for shop in self.shops:
						if shop.x == x1 + x and shop.y == y1 + y:
							shop.shop(obj) # selects and runs shop interface in items.py
							return True
				elif self.map[y1 + y][x1 + x] == "E": # initailises battle
					self.map[y1][x1] = " " # move onto enemy
					obj.x += x
					obj.y += y
					return 'battle'
				else:
					return False
			elif obj.__class__.__name__ == "Ai_group": # if is enemy
				if self.map[y1 + y][x1 + x] == 'X': # make battle on player
					self.map[y1][x1] = " "
					obj.x += x
					obj.y += y
					return 'battle'
				else:
					return False # break if its not valid
		except IndexError:
			return False

	def run(self):
		"""Runs the battle map"""
		while True:
			situation, player, leave = self.player_move()
			if leave == True:
				return None, True
			elif situation == 'battle':
				return player, False
			elif situation == 'shop':
				player.run(player)
			enemies = self.ai_move()
			if enemies:
				return enemies, False


	def player_move(self):
		"""Player move user interface"""
		while True:
			self.draw() # draws map
			# gives instructions
			self.app.write("Choose a direction to move! (wasd or hjkl(vim style))")
			self.app.write("Press 0 to pass your move")
			self.app.write("")
			self.app.wait_variable(self.app.inputVariable)
			move = self.app.inputVariable.get()
			try:
				# processes input simmilarly to battle map
				if move == '0':
					pass
				elif move == "quit":
					self.app.quit()
				elif move == "w" or move == "j":
					move = self.check(-1, 0, self.player)
				elif move == "s" or move == "k":
					move = self.check(1, 0, self.player)
				elif move == "a" or move == "h":
					move = self.check(0, -1, self.player)
				elif move == "d" or move == "l":
					move = self.check(0, 1, self.player)
				else:
					raise ValueError
				if move == 'battle': # if battle
					for enemy in self.enemies: # find enemy
						if enemy.x == self.player.x and enemy.y == self.player.y:
							enemies = enemy.enemies
							self.enemies.remove(enemy) # delete enemy
							return 'battle', enemies, False # make battle
				elif move == True:
					return False, None, False
			except ValueError:
				self.app.write("Invalid Input")

	def ai_move(self):
		"""AI moving algorithm"""
		for group in self.enemies:# iterates through enemies
			move = False
			playerclose = False
			while not move: # while not false
				if abs(self.player.x - group.x) < 16 and abs(self.player.y - group.y) < 32: # if player within 16 by 32
					# move towards player
					playerclose = True
					if self.player.x > group.x:
						x_change = 1
					elif self.player.x < group.x:
						x_change = -1
					else:
						x_change = 0

					if self.player.y > group.y:
						y_change = 1
					elif self.player.y < group.y:
						y_change = -1
					else:
						y_change = 0
				else: # else brute force
					x_change = random.randint(-1, 1)
					y_change = random.randint(-1, 1)
				move = self.check(y_change, x_change, group)
				if move == 'battle': # if battle
					enemies = group.enemies
					self.enemies.remove(group)
					return enemies # do battle
				elif playerclose == True and move == False:
					return None



class Ai_group(object):
	"""AI case for battle map"""
	def __init__(self, x, y, enemies):
		self.x = x
		self.y = y
		self.enemies = enemies

class Player_group(object):
	def __init__(self, x, y, players):
		"""Player case for battle map"""
		self.x = x
		self.y = y
		self.players = players


""" BELOW IS UNFINISHED/BROKEN GENERATOR IMPLEMENTATION """

# class Room(object):
# 	"""Room Object ~
# 		Keeps data for a single room in the
# 		map with data such as size and type
# 	"""
# 	def __init__(self, x1, y1, x2, y2, base):
# 		"""initialiser for Room Object"""
# 		self.points = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
# 		self.area = abs(x1-x2) * abs(y1-y2)
# 		self.centrePoint = [int((x1 + x2)/2), int((y1 + y2)/2)]
# 		self.repr = base

# 	def create(self):
# 		""" Create Method ~
# 		draws the object onto a blank map
# 		for merger process
# 		"""
# 		for j in range(int(self.points[0][0]), int(self.points[2][0])):
# 				for k in range(self.points[0][1], self.points[2][1]):
# 					self.repr[j][k] = 1

# 		return self.repr

# 	def checkOverlap(self, room):
# 		"""Check overlap Method ~
# 		this method takes in another room object and returns if the two rooms
# 		are overlapping or not. This method is used in Map object's moveBoxes method
# 		"""
# 		intercept = []
# 		for i, point in enumerate(self.points):
# 			if point[0] in range(room.points[0][0], room.points[2][0])\
# 			and point[1] in range(room.points[0][1], room.points[2][1]):
# 				intercept.append(i)
# 		if len(intercept):
# 			return True, intercept
# 		else:
# 			return False, None

# class Generator(object):
# 	"""Generator object ~S
# 		This object generates the map and keeps track of its current situation
# 	"""

# 	def __init__(self, size=255, rooms=40):
# 		"""Initialiser for Map"""
# 		self.x = size if size > 64 else 64
# 		self.y = size if size > 64 else 64
# 		self.rooms = rooms
# 		self.map = make_map(self.x, self.y, 0)
# 		self.roomlst = []
# 		self.hubs = []


# 	def randomPoint(self):
# 		"""random Point Method ~
# 		Selects a random point within defined space
# 		"""
# 		# mid rect width, height 20%
# 		x = random.randint(abs((self.x / 2) - self.x / 8),
# 						   abs((self.x / 2) + self.x / 8))
# 		y = random.randint(abs((self.y / 2) - self.y / 8),
# 						   abs((self.y / 2) + self.y / 8))
# 		return x, y


# 	def generate(self):
# 		"""generate Method ~
# 		Contains the correct order of calls for a map to be generated.
# 		 -> Called in the initaliser
# 		"""
# 		self.createBoxes()
# 		self.moveBoxes()
# 		self.chooseMainRooms()
# 		self.triangulate()


# 	def createBoxes(self):
# 		""" Create Boxes method
# 		This method creates a bunch of boxes in a small space on
# 		the map. This allows for the initial generation of the
# 		rooms on the map before the moveBoxes method is called.
# 		"""
# 		for i in range(self.rooms):
# 			x1, y1 = self.randomPoint()
# 			x2, y2 = self.randomPoint()
# 			a = Room(x1, y1, x2, y2, self.map)
# 			self.roomlst.append(a)


# 	def moveBoxes(self):
# 		""" Move Boxes Method ~
# 		This method is used to separate all the overlapping boxes
# 		created by the Create boxes method. This it to allow for
# 		the rooms to finalise their position in the maze before
# 		the rooms are purged.
# 		"""
# 		moving = True
# 		exits = []
# 		while moving: # while moving boxes
# 			for i, room in enumerate(self.roomlst): # grab each room and index
# 				for roomIndex in range(0, i): # loop through every room below current
# 					room2 = self.roomlst[roomIndex] # shortens handle
# 					overlap, pnts = room.checkOverlap(room2) # checks for overlap
# 					if overlap: # if overlapping
# 						x_dist, y_dist = [], [] # inits 2 lists
# 						# iterates through only overlapping points
# 						for i, point in [(i, room.points[x]) for i, x in enumerate(pnts)]:
# 							x1 = point[0] # takes X of point
# 							y1 = point[1] # takes Y of point
# 							for point1 in room2.points: #iterates through points in second room
# 								x2 = point1[0] # takes X of point
# 								y2 = point1[1] # takes Y of point
# 								x3 = abs(x1 - x2) # find difference
# 								y3 = abs(y1 - y2) # find difference
# 								x_dist.append((i, x3)) # appends difference and origianl point value
# 								y_dist.append((i, y3)) # appends difference and origianl point value

# 						if max([x[1] for x in x_dist]) > max([y[1] for y in y_dist]):
# 							list_x = [x[1] for x in x_dist]
# 							index = list_x.index(max(list_x))
# 							point = room.points[x_dist[index][0]] - 1
# 							bot_x = room2.points[0][0] if room2.points[0][0] < room2.points[1][0] else room2.points[1][0] # takes Lowest x value of room2
# 							top_x = room2.points[0][0] if room2.points[0][0] < room2.points[1][0] else room2.points[1][0] # takes Highest x value of room2
# 							dist_up = abs(top_x - point[0])
# 							dist_down = abs(bot_x - point[0])
# 							for point in room.points:
# 								if dist_up > dist_down:
# 									point[0] += dist_up
# 								else:
# 									point[0] += dist_down

# 						else:
# 							list_y = [y[1] for y in y_dist]
# 							index = list_y.index(max(list_y))
# 							point = room.points[y_dist[index][0] - 1]
# 							bot_y = room2.points[0][1] if room2.points[0][1] < room2.points[1][1] else room2.points[1][1] # takes Lowest Y value of room2
# 							top_y = room2.points[0][1] if room2.points[0][1] < room2.points[1][1] else room2.points[1][1] # takes Highest Y value of room2
# 							dist_up = abs(top_y - point[1])
# 							dist_down = abs(bot_y - point[1])
# 							for point in room.points:
# 								if dist_up > dist_down:
# 									point[1] += dist_up
# 								else:
# 									point[1] += dist_down

# 			exits = []
# 			for i, room in enumerate(self.roomlst): # grab each room and index
# 				for roomIndex in range(i, len(self.roomlst)): # loop through all rooms after current
# 					if room.checkOverlap(self.roomlst[roomIndex]): # if they overlap
# 						exits.append(True)
# 						break # start again
# 					else:
# 						exits.append(False)
# 			if True in exits:
# 				break

# 	def chooseMainRooms(self):
# 		avg = sum([room.area for room in self.roomlst])/len(self.roomlst)*1.25
# 		for room in self.roomlst:
# 			if room.area >= avg:
# 				self.hubs.append(room)
# 				self.roomlst.remove(room)


# 	def triangulate(self):
# 		centrePoints = []
# 		for room in self.hubs:
# 			centrePoints.append(room.centrePoint)
# 		print(centrePoints)
# 		points = array(centrePoints, dtype='int8')
# 		triangles = Delaunay(points)
# 		print(points[triangles.simplices])
# 		tree = minimum_spanning_tree(points[triangles.simplicies])
		# ! WORK HERE
# 		print(dir(triangles))



# if __name__ == '__main__':
# 	a = Generator(128, 50)
# 	a.generate()
# 	# for room in a.hubs:
# 	# 	print(room.points)
# 	# 	print(room.area)
# 	# 	print(room.centrePoint)
# 	print("YAY")
