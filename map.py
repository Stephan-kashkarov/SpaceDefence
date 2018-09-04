#!/usr/local/bin/python3.6
import math
import random
from pprint import pprint


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


class Map(object):
	"""Map object ~ 
		This object generates the map and
		keeps the location of all the important
		landmarks and characters 
	"""

	def __init__(self, x=255, y=255, size=10):
		"""Initialiser for Map"""
		self.x = x if x > 128 else 128
		self.y = y if y > 128 else 128
		self.size = size
		self.map = []
		self.rooms = []
		for i in range(self.x):
			self.map.append([])
			for j in range(self.y):
				self.map[i].append(0)

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
		for i in range(self.size):
			x1, y1 = self.randomPoint()
			x2, y2 = self.randomPoint()
			a = Room(x1, y1, x2, y2, self.map)
			self.rooms.append(a)


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
			for i, room in enumerate(self.rooms): # grab each room and index
				print("First | i: {}, room: {}". format(i, room))
				for roomIndex in range(0, i): # loop through every room below current
					room2 = self.rooms[roomIndex] # shortens handle
					x = room.x1 - room2.x1 # detects run
					y = room.y1 - room2.y1 # detects rise
					overlap = room.checkOverlap(room2)
					while overlap: # while the rooms are still overlapping
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
			for i, room in enumerate(self.rooms): # grab each room and index
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








# testing

if __name__ == '__main__':
	a = Map(128, 128)
	a.generate()
