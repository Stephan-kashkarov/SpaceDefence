#!/usr/local/bin/python3
"""
rpg.py - entry point for the RPG Game

Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2015
Modified with permission by Edwin Griffin for
Intermediate Programming Object-Oriented Assignment 2018
"""

# import modules
import sys
import map_
import time
import random


class Battle:

	def __init__(self, players, enemies, app):
		"""
		Instantiates a battle object between the players and enemies specified,
		sending output to the given gui instance
		"""
		self.players = players
		self.enemies = enemies
		self.app = app
		self.turn = 1
		self.wins = 0
		self.kills = 0
		self.player_won = False
		self.player_lost = False
		self.losses = []
		self.battle_map = map_.make_map(16, 16, " ", boundry=True)
		self.spawnpoints = []
		self.generate()
		self.select_spawnpoints()


	def play(self):
		"""
		Begins and controls the battle
		returns tuple of (win [1 or 0], no. kills)
		"""
		
		while not self.player_won and not self.player_lost: # while game
			
			self.app.write("Turn "+str(self.turn))
			self.app.write("")
			
			# This is where the bulk of the battle takes place
			#player actionq
			flee = self.do_player_actions()
			if flee: # checks for flee
				return (self.wins, self.kills, False)

			# enemy action
			loss = self.do_enemy_actions()
			if loss:
				return (self.wins, self.kills, True)
			
			# advance turn counter
			self.turn += 1
			
		return (self.wins, self.kills, False)


	def get_action(self, player):
		""" Gets the player's chosen action for their turn """
		while True:
			try:
				self.app.write(player.name + "'s Turn:")
				self.app.write("	1. Attack Enemies")
				self.app.write("	2. Use Abilities")
				self.app.write("	3. Use Items")
				self.app.write("	4. Move")
				self.app.write("	5. Pass")
				self.app.write("	0. Flee the battle")
				self.app.write("")
				self.app.wait_variable(self.app.inputVariable)
				player_action = self.app.inputVariable.get()

				if player_action == 'quit':
					self.app.quit()

				# validate response
				player_action = int(player_action)
				if player_action not in range(0,6):
					raise ValueError
				else:
					break

			except ValueError:
				self.app.write("You must enter a valid choice")
				self.app.write("")
		
		return player_action


	def select_ability(self, player):
		""" Selects the ability the player would like to use """
		player_race = player.__class__.__name__

		while True:
			try:
				# defines input
				self.app.write("Select your ability:")
				if player_race in ["Ethereal","Psionic"] and player.adrenaline >= 10:
					self.app.write("	1. Throw (10 ap)")
				if player.adrenaline >= 20:
					self.app.write("	2. Shield (20 ap)")
				if (player.mind > 10 or player.level > 5) and player_race in ["Queen", 'Ethereal']:
					self.app.write("	3. Stun (5 ap)")
				self.app.write("	0. Back")
				self.app.write("")
				self.app.wait_variable(self.app.inputVariable)
				ability_choice = self.app.inputVariable.get()

				# validates input
				if ability_choice == 'quit':
					self.app.quit()
				ability_choice = int(ability_choice)
				if ability_choice == 0:
					return False
				valid_ability = player.valid_ability(ability_choice)
				if not valid_ability:
					raise ValueError
				else:
					break
					
			except ValueError:
				self.app.write("You must enter a valid choice")
				self.app.write("")
		
		return ability_choice


	def select_item(self, player):
		""" Selects the item the player would like to use """
		
		while True:
			try:
				#defines input
				self.app.write("Select an Item:")
				if len(player.inventory) > 0:
					#lists all items player can use
					for i, item in enumerate(player.inventory):
						self.app.write("	{}. {} ({} ~ available)".format(i, item.name, item.ammount))
				else:
					self.app.write("	No items in inventory")
				self.app.write("	e. exit")
				self.app.wait_variable(self.app.inputVariable)
				item_choice = self.app.inputVariable.get()

				if item_choice == "quit":
					self.app.quit()

				elif item_choice == "e":
					return item_choice

				elif int(item_choice) in range(len(player.inventory)):
					return int(item_choice)

				else:
					raise ValueError


			except ValueError:
				self.app.write("You must enter a valid choice")
				self.app.write("")

	def use_item(self, player, index):
		"""Uses an item selected by a player"""
		item = player.inventory[index] # selects item
		use = item.use(player) # runs item use function
		if use: # if item was succsessfully used
			self.app.write("{} has used a/an {}".format(player.name, item.name))
			return True
		else:  # if item wasn't succsessfully used
			self.app.wrte("{} has no more {}s".format(player.name, item.name))
			return False

	def choose_target(self, player):
		""" Selects the target of the player's action """
		while True:
			# creates a list of valid targets
			enemies = [x for x in self.enemies] # makes a copy of enemies list
			for i, enemy in [x for x in enumerate(enemies)][::-1]: # loops through enemies and indexes backwards
				if not self.can_see(player, enemy)[0] or enemy.health <= 0: # if enemy is not in line of sight
					enemies.pop(i) #remoces enemy from the list (by index and thats why i go backwards)
			try:
				self.app.write("Choose your target:")
				if len(enemies) == 0:
					self.app.write("No enemies visible!")
				else:
					# use j to give a number option
					j = 0
					while j < len(enemies): # lists all emeies
						self.app.write("{}. {} (Cover: {:.2f})".format(
							str(j + 1),
							enemies[j].name,
							self.can_see(player, enemies[j])[1]
						))
						j += 1
				self.app.write("0. Cancel")
				self.app.write("")
				self.app.wait_variable(self.app.inputVariable)
				target = self.app.inputVariable.get()


				# validates input
				if target == 'quit':
					self.app.quit()

				target = int(target)
				if target == 0:
					return False
				else:
					target -= 1

				if not (target < len(self.enemies)):
					raise ValueError
				else:
					break
					
			except ValueError:
				self.app.write("You must enter a valid choice")
				self.app.write("")

		return target + 1


	def choose_stance(self):
		"""Selects stance of char"""
		while True:
			try:
				#defines input
				self.app.write("Choose your stance:")
				self.app.write("	a - Aggressive")
				self.app.write("	d - Defensive")
				self.app.write("	b - Balanced")
				self.app.write("")
				self.app.wait_variable(self.app.inputVariable)
				stance_choice = self.app.inputVariable.get()

				#validates input
				if stance_choice == 'quit':
					self.app.quit()

				if stance_choice not in ['a','d','b'] or stance_choice == '':
					raise ValueError
				else:
					break

			except ValueError:
				self.app.write("You must enter a valid choice")
				self.app.write("")
		
		return stance_choice

	def draw_map(self, player):
		"""Draws the battle map"""
		self.app.write("\n\n\n\n\n\n\n\n\n\n\n\n") # visual separation
		self.app.write("XXXXXXXXXXXXXXXXXX") # top row
		for i in range(player.battleY - 8, player.battleY + 8): # draws 8 either side of char
			visible_map = 'X' # fitst wall char
			for j in range(player.battleX - 8, player.battleX + 8):  # draws 8 either side of char
				if j < 0 or i < 0: # if index below range
					visible_map += "."
				elif j == player.battleX and i == player.battleY:
					visible_map += "x" # draws player
				else:
					try:
						visible_map += str(self.battle_map[i][j])
					except: # if index out of range
						visible_map += "."
			visible_map += "X"
			self.app.write(visible_map)
		self.app.write("XXXXXXXXXXXXXXXXXX") # bottom row


	def map(self, player, team):
		"""Run map function ~ runs the map for the player"""
		while True:
			self.draw_map(player) # draws map
			try:
				# gets input
				self.app.write("Move: (wasd or hjkl(vim style))")
				self.app.write("0. Cancel")
				self.app.write("")
				self.app.wait_variable(self.app.inputVariable)
				move = self.app.inputVariable.get()

				# validates input
				if move == '0':
					self.battle_map[player.battleY][player.battleX] = team
					return False
				elif move == "quit":
					self.app.quit()


				# checks directional move and excicutes
				elif move == "w" or move == "j":
					move = self.move(-1, 0, player)
				elif move == "s" or move == "k":
					move = self.move(1, 0, player)
				elif move == "a" or move == "h":
					move = self.move(0, -1, player)
				elif move == "d" or move == "l":
					move = self.move(0, 1, player)
				else:
					raise ValueError
				
				# checks result of move
				if move == 1:
					self.app.write("Not enough adrenaline to move!")
					self.app.write("")
					self.battle_map[player.battleY][player.battleX] = team
					return True

				# invalid move
				elif move == 2:
					raise ValueError

			except ValueError:
				self.app.write("Invalid response/Move")
				self.app.write("")

	def ai_map(self, enemy):
		"""AI algorithm for map nva"""
		players = [self.can_see(enemy, player) for player in self.players] # list of visible players objects
		playersTF = [self.can_see(enemy, player)[0] for player in self.players] # True/False (T/F) list of visible players
		i = 0
		while True not in playersTF and i < 200: # limits infinate resrsion if char cannot move
			self.draw_map(enemy) # draws map for the enemy
			time.sleep(0.5) # tiny break
			while True:
				if True not in playersTF: # if no players visible
					if random.randint(0,1) == 1: # choose x or y movement
						x = random.randint(-1, 1)
						y = 0
					else:
						x = 0
						y = random.randint(-1, 1)
					res = self.move(y, x, enemy) # checks move
					playersTF = [self.can_see(enemy, player)[0] for player in self.players] # updates visible players T/F
					if True in playersTF: # checks visible players
						break
					if res == 0: # if move successfull
						self.battle_map[enemy.battleY][enemy.battleX] = "E"
						break
					else: # iterate timer till exit conditon if the char hasnt moved
						i += 1
						if i > 200:
							break
				else:
					while True: # moves towards visible player till out of adrenaline
						index = random.randint(0, len(players) - 1) # selects random player
						player = players[index]
						if player[0] == True: # if player is visible
							player = player[2] # takes player object
							break
					while enemy.adrenaline >= 0: # moves untill out of adrenaline
						if random.randint(0, 1) == 1: # rand x or y
							x = 1 if player.battleX < enemy.battleX else -1
							y = 0
						else:
							x = 0
							y = 1 if player.battleY < enemy.battleY else -1
						res = self.move(y, x, enemy) # moves
						if res == 0:
							self.battle_map[enemy.battleY][enemy.battleX] = "E"
							break
						else:
							i += 1
							if i > 200:
								break
					break

		# creates list of players and returns them
		output = []
		for i, val in enumerate(players):
			if val != False:
				output.append(self.players[i])
		return output




	def move(self, y, x, player):
		# takes x and y
		x1 = player.battleX
		y1 = player.battleY
		try:
			# checks for valid move
			if self.battle_map[y1 + y][x1 + x] == " " and player.adrenaline >= 5:
				self.battle_map[y1][x1] = " "
				self.battle_map[y1 + y][x1 + x] = "X"
				player.battleX += x
				player.battleY += y
				player.adrenaline -= 5
				return 0 # move successful
			elif player.adrenaline < 5:
				return 1 # out of adrenaline
			else:
				return 2 # invalid move
		except IndexError:
			return 2  # invalid move


	def generate(self):
		"""generate Method ~
		This method generates a battle map for the
		current battle. The map contains:
		 ~ 2 buildings
		 ~ 8 benches
		 ~ a few friendly spawn points
		 ~ a few enemy spawn points
		"""
		# creates locals
		benches = [] 
		buildings = []

		# generates buildings
		while len(buildings) <= 1:
			# randomises x and y
			x = random.randint(5, len(self.battle_map) - 7) 
			y = random.randint(5, len(self.battle_map[0]) - 7)
			# if empty tile
			if self.battle_map[y][x] == " ":
				# appends building to list
				buildings.append((x, y))
				# generates building
				for i in range(x, x + 5):
					for j in range(y, y + 5):
						self.battle_map[j][i] = "B"
		del buildings # delets building list to save memory and cos using del is cool

		# generates light cover
		while len(benches) <= 8:
			# randomises x and y
			x = random.randint(3, len(self.battle_map) - 5)
			y = random.randint(3, len(self.battle_map[0]) - 5)
			type = random.randint(0, 1) # selects orientation of cover
			if self.battle_map[y][x] == " ":
				benches.append((x, y, type))
				if type == 1:
					for i in range(x, x + 3): # horizontal cover
						self.battle_map[y][i] = 'o'
				else:
					for i in range(y, y + 3): # vertical cover
						self.battle_map[i][x] = 'o'
		del benches  # delets building list to save memory even though it will be deleted by next line anyway and cos using del is cool


	def select_spawnpoints(self):
		"""Selects spawnpoints on map"""
		for i in self.players:
			# for each player
			while True:
				# randomises untill empty tile
				x = random.randint(
						1,
						(len(self.battle_map) - 1) / 4
					)
				y = random.randint(
						1,
						(len(self.battle_map[0]) - 1) / 4
					)
				if self.battle_map[y][x] == " ":
					self.battle_map[y][x] = 'A'
					break
			# sets player obj x and y
			i.battleX = x 
			i.battleY = y
		for i in self.enemies:
			# for each enemy
			while True:
				# randomises untill empty tile
				x = random.randint(
						int(3/4 * len(self.battle_map)) -1,
						len(self.battle_map) - 2
					)
				y = random.randint(
						int(3/4 * len(self.battle_map[0])) - 1,
						len(self.battle_map[0]) - 2
					)
				if self.battle_map[y][x] == " ":
					self.battle_map[y][x] = 'E'
					break
			# sets enemy obj x and y
			i.battleX = x
			i.battleY = y
			


	def can_see(self, player1, player2):
		"""Can see function returns wether or not two players can see eachother on may and other player obj"""
		if player2.battleX != player1.battleX: # Zero div error check
			# generates gradient
			gradient =  (player2.battleY - player1.battleY) /\
						(player2.battleX - player1.battleX)
		else:
			gradient = 0
		# generates intercept
		intercept = player1.battleY - (gradient * player1.battleX)
		# selects algorithm for x or y
		if player1.battleY != player2.battleY:
			modifier = 100 # sets mod to 100%
			for y in range(player1.battleY, player2.battleY, (1) if player2.battleY > player1.battleY else (-1)): # iterates through y values between objs
				if gradient == 0:
					x = y
				else:
					x = int((y - intercept) / gradient) # calculates x value
				modifier = self.get_mod(x, y, modifier) # gets modifier update for coord
				if modifier == 0: # if cover = 100% exit
					break

		else: # x axis calc
			modifier = 100
			for x in range(player1.battleX, player2.battleX, 1 if player1.battleX < player2.battleX else -1):
				y = int((gradient * x) + intercept)
				modifier = self.get_mod(x, y, modifier)
				if modifier == 0:
					break
		return (True, modifier, player2) if modifier > 0 else (False, 0, player2) # returns true unless mod is 0 else false

	def get_mod(self, x, y, modifier):
		"""Calc modifier at a point"""
		if self.battle_map[y][x] == " ": # if empty
			if modifier >= 5:
				modifier -= 5
			else:
				return 0
		elif self.battle_map[y][x] == "B": # if building break
			return 0
		elif self.battle_map[y][x] == "o": # if light cover lower a bit
			if modifier >= 45:
				modifier -= 45
			else:
				return 0
		else: # if player obj lower a bit less
			if modifier >= 35:
				modifier -= 35
			else:
				return 0
		return modifier


	def do_player_actions(self):
		""" Performs the player's actions """
	
		turn_over = False
	
		while not self.player_won and not turn_over: # while turn
			
			for player in self.players: # iterates players
				if player.stunned == True: # if player is stunned skip turn
					player.stunned = False
				else:
					while True:
						# print stuff
						player.print_status()
						stance_choice = self.choose_stance()
						player.set_stance(stance_choice)
						
						# gets input
						player_action = self.get_action(player)

						has_attacked = False

						if player_action == 5: # passes turn
							has_attacked = True

						elif player_action == 4: # moves around map
							has_attacked = self.map(player, "A")

						elif player_action == 3: # opens inventory
							item_choice = self.select_item(player)
							if item_choice != "e":
								self.use_item(player, item_choice)
							has_attacked = False

						elif player_action == 2: # selects abilities
							ability_choice = self.select_ability(player)

							if ability_choice != 0: # if not cancel
								has_attacked = True
								if ability_choice == 1 or ability_choice == 3: # if ability requires target
									target = self.choose_target(player) # select target
									if target == 0: # if cancel
										has_attacked = False
									else:
										target -= 1 # correct indexing
										if player.use_ability(ability_choice, self.enemies[target]): # if enemy died 
											self.kills += 1
								else:
									player.use_ability(ability_choice) # use targetless ability
							
						elif player_action == 0: # if player flees
							return True # exit and make flee true

						else: # attack option
							target = self.choose_target(player) # selects target
							if target == False: # cancels
								has_attacked = False
							else:
								target -= 1 # corrects indexing
								has_attacked = True
								modifier = self.can_see(player, self.enemies[target])[1] # gets full modifier between two enemies

								if player.attack_enemy(self.enemies[target], modifier): # attacks with modifier and returns if killed or not
									self.kills += 1
									self.app.write("{} was awarded 20 gold".format(player.name))
									player.money += 20 # kill bonus
									# transfers inventories
									self.app.write("{} has dropped some items:".format(self.enemies[target]))
									for item in target.inventory:
										self.app.write("	{}".format(item.name))
										name = item.__class__.__name__
										for item2 in player.inventory:
											name2 = item2.__class__.__name__
											if name == name2:
												item2.ammount += item.ammount
												item.ammount = 0

						# checks for turn over
						turn_over = True 
						if not has_attacked:
							turn_over = False
						else:
							# resets adrenaline
							player.adrenaline = player.max_adrenaline
							self.player_won = True
							# checks for vicotry
							for enemy in self.enemies:
								if enemy.health > 0:
									self.player_won = False
									break

							if self.player_won == True:
								self.app.write("Your enemies have been vanquished!!")
								self.app.write("")
								time.sleep(1)
								self.wins += 1
								break

						if turn_over:
							break

	def do_enemy_actions(self):
		""" Performs the enemies' actions """

		# if game
		if not self.player_won:
			self.app.write("Enemies' Turn:")
			self.app.write("")
			time.sleep(1)

			for enemy in self.enemies: # iteates enemies
				if enemy.health > 0 and not self.player_lost:
					if enemy.stunned == True: # check stunned
						enemy.stunned = False
					else:
						players = [x for x in self.players] # makes copy of players list
						for player in players: # Creates visible enemies list
							if not self.can_see(enemy, player)[0]:
								players.remove(player)
						# if game again
						if not self.player_lost: 
							if len(players) == 0: # if no emeies visible
								players = self.ai_map(enemy) # go look for them
							if len(players) != 0: #other wise pick a random one and attack
								player_index = random.randint(0, len(players) - 1)
								player = players[player_index]
								mod = self.can_see(enemy, player) # get modifier from map
								loss = enemy.move(player, mod[1])
								self.losses.append(loss)
								if loss == True: # when you kill sombody
									self.app.write(
											"{} the {} has perished on the field of battle".format(
												player.name, player.__class__.__name__
											)
										)
									self.app.write("")
									time.sleep(1)
									game_over = True
									for player in self.players:
										if player.health > 0:
											game_over = False # checks if any players are alive at all
									if game_over: # when game ends
										self.player_lost = True
										self.app.write("Your party has been killed by your enemies.")
										self.app.write("")
										time.sleep(1)
										self.player_lost = True
										return True
				enemy.adrenaline = enemy.max_adrenaline # resets adrenaline
