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
		
		while not self.player_won and not self.player_lost:
			
			self.app.write("Turn "+str(self.turn))
			self.app.write("")
			
			# This is where the bulk of the battle takes place
			flee = self.do_player_actions()
			if flee:
				return (self.wins, self.kills, False)
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
				self.app.write("Select an Item:")
				if len(player.inventory) > 0:
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
		item = player.inventory[index]
		use = item.use(player)
		if use:
			self.app.write("{} has used a/an {}".format(player.name, item.name))
			return True
		else:
			self.app.wrte("{} has no more {}s".format(player.name, item.name))
			return False

	def choose_target(self, player):
		""" Selects the target of the player's action """
		while True:
			enemies = [x for x in self.enemies]
			for i, enemy in [x for x in enumerate(enemies)][::-1]:
				if not self.can_see(player, enemy)[0] or enemy.health <= 0:
					enemies.pop(i)
			try:
				self.app.write("Choose your target:")
				if len(enemies) == 0:
					self.app.write("No enemies visible!")
				else:
					# use j to give a number option
					j = 0
					while j < len(enemies):
						self.app.write("{}. {} (Cover: {:2f})".format(
							str(j + 1),
							enemies[j].name,
							self.can_see(player, enemies[j])[1]
						))
						j += 1
				self.app.write("0. Cancel")
				self.app.write("")
				self.app.wait_variable(self.app.inputVariable)
				target = self.app.inputVariable.get()

				if target == 'quit':
					self.app.quit()

				target = int(target)
				if target == 0:
					return False
				else:
					target += 1
				if not (target < len(self.enemies)):
					raise ValueError
				else:
					break
					
			except ValueError:
				self.app.write("You must enter a valid choice")
				self.app.write("")

		return target + 1


	def choose_stance(self):
		while True:
			try:
				self.app.write("Choose your stance:")
				self.app.write("	a - Aggressive")
				self.app.write("	d - Defensive")
				self.app.write("	b - Balanced")
				self.app.write("")
				self.app.wait_variable(self.app.inputVariable)
				stance_choice = self.app.inputVariable.get()

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
		self.app.write("\n\n\n\n\n\n\n\n\n\n\n\n")
		self.app.write("XXXXXXXXXXXXXXXXXX")
		for i in range(player.battleY - 8, player.battleY + 8):
			visible_map = 'X'
			for j in range(player.battleX - 8, player.battleX + 8):
				if j < 0 or i < 0:
					visible_map += "."
				elif j == player.battleX and i == player.battleY:
					visible_map += "x"
				else:
					try:
						visible_map += str(self.battle_map[i][j])
					except:
						visible_map += "."
			visible_map += "X"
			self.app.write(visible_map)
		self.app.write("XXXXXXXXXXXXXXXXXX")


	def map(self, player, team):
		while True:
			self.draw_map(player)
			try:
				self.app.write("Move: (wasd or hjkl(vim style))")
				self.app.write("0. Cancel")
				self.app.write("")
				self.app.wait_variable(self.app.inputVariable)
				move = self.app.inputVariable.get()

				if move == '0':
					self.battle_map[player.battleY][player.battleX] = team
					return False
				elif move == "quit":
					self.app.quit()
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
				
				if move == 1:
					self.app.write("Not enough adrenaline to move!")
					self.app.write("")
					self.battle_map[player.battleY][player.battleX] = team
					return True
				elif move == 2:
					raise ValueError

			except ValueError:
				self.app.write("Invalid response/Move")
				self.app.write("")

	def ai_map(self, enemy):
		players = [self.can_see(enemy, player) for player in self.players]
		playersTF = [self.can_see(enemy, player)[0] for player in self.players]
		i = 0
		while True not in playersTF and i < 200:
			self.draw_map(enemy)
			time.sleep(0.5)
			while True:
				if True not in playersTF:
					if random.randint(0,1) == 1:
						x = random.randint(-1, 1)
						y = 0
					else:
						x = 0
						y = random.randint(-1, 1)
					res = self.move(y, x, enemy)
					playersTF = [self.can_see(enemy, player)[0] for player in self.players]
					if True in playersTF:
						break
					if res == 0:
						self.battle_map[enemy.battleY][enemy.battleX] = "E"
						break
					else:
						i += 1
						if i > 200:
							break
				else:
					while True:
						index = random.randint(0, len(players) - 1)
						player = players[index]
						if player[0] == True:
							player = player[2]
							break
					while enemy.adrenaline >= 0:
						if random.randint(0, 1) == 1:
							x = 1 if player.battleX < enemy.battleX else -1
							y = 0
						else:
							x = 0
							y = 1 if player.battleY < enemy.battleY else -1
						res = self.move(y, x, enemy)
						if res == 0:
							self.battle_map[enemy.battleY][enemy.battleX] = "E"
							break
						else:
							i += 1
							if i > 200:
								break
					break

		output = []
		for i, val in enumerate(players):
			if val != False:
				output.append(self.players[i])
		return output




	def move(self, y, x, player):
		x1 = player.battleX
		y1 = player.battleY
		try:
			if self.battle_map[y1 + y][x1 + x] == " " and player.adrenaline >= 5:
				self.battle_map[y1][x1] = " "
				self.battle_map[y1 + y][x1 + x] = "X"
				player.battleX += x
				player.battleY += y
				player.adrenaline -= 5
				return 0
			elif player.adrenaline < 5:
				return 1
			else:
				return 2
		except IndexError:
			return 2


	def generate(self):
		"""generate Method ~
		This method generates a battle map for the
		current battle. The map contains:
		 ~ 2 buildings
		 ~ 8 benches
		 ~ a few friendly spawn points
		 ~ a few enemy spawn points
		"""
		self.initailised = True
		benches = []
		buildings = []
		while len(buildings) <= 1:
			x = random.randint(5, len(self.battle_map) - 7)
			y = random.randint(5, len(self.battle_map[0]) - 7)
			if self.battle_map[y][x] == " ":
				buildings.append((x, y))
				for i in range(x, x + 5):
					for j in range(y, y + 5):
						self.battle_map[j][i] = "B"
		del buildings
		while len(benches) <= 8:
			x = random.randint(3, len(self.battle_map) - 5)
			y = random.randint(3, len(self.battle_map[0]) - 5)
			type = random.randint(0, 1)
			if self.battle_map[y][x] == " ":
				benches.append((x, y, type))
				if type == " ":
					for i in range(x, x + 3):
						self.battle_map[y][i] = 'o'
				else:
					for i in range(y, y + 3):
						self.battle_map[i][x] = 'o'
		del benches


	def select_spawnpoints(self):
		for i in self.players:
			while True:
				x = random.randint(
						1,
						(len(self.battle_map) - 1) / 4
					)
				y = random.randint(
						1,
						(len(self.battle_map[0]) - 1) / 4
					)
				if self.battle_map[y][x] == " ":
					self.spawnpoints.append((x, y, 1))
					self.battle_map[y][x] = 'A'
					break
			i.battleX = x
			i.battleY = y
		for i in self.enemies:
			while True:
				x = random.randint(
						int(3/4 * len(self.battle_map)) -1,
						len(self.battle_map) - 2
					)
				y = random.randint(
						int(3/4 * len(self.battle_map[0])) - 1,
						len(self.battle_map[0]) - 2
					)
				if self.battle_map[y][x] == " ":
					self.spawnpoints.append((x, y, 2))
					self.battle_map[y][x] = 'E'
					break
			i.battleX = x
			i.battleY = y
			


	def can_see(self, player1, player2):
		if player2.battleX != player1.battleX:
			gradient = (player2.battleY - player1.battleY) /\
					   (player2.battleX - player1.battleX)
		else:
			gradient = 0
		intercept = player1.battleY - (gradient * player1.battleX)
		if player1.battleY != player2.battleY:
			modifier = 100
			for y in range(player1.battleY, player2.battleY, (1) if player2.battleY > player1.battleY else (-1)):
				if gradient == 0:
					x = y
				else:
					x = int((y - intercept) / gradient)
				modifier = self.get_mod(x, y, modifier)
				if modifier == 0:
					break

		else:
			modifier = 100
			for x in range(player1.battleX, player2.battleX, 1 if player1.battleX < player2.battleX else -1):
				y = int((gradient * x) + intercept)
				modifier = self.get_mod(x, y, modifier)
				if modifier == 0:
					break
		return (True, modifier, player2) if modifier > 0 else (False, 0, player2)

	def get_mod(self, x, y, modifier):
		if self.battle_map[y][x] == " ":
			if modifier >= 5:
				modifier -= 5
			else:
				return 0
		elif self.battle_map[y][x] == "B":
			return 0
		elif self.battle_map[y][x] == "o":
			if modifier >= 45:
				modifier -= 45
			else:
				return 0
		else:
			if modifier >= 35:
				modifier -= 35
			else:
				return 0
		return modifier


	def do_player_actions(self):
		""" Performs the player's actions """
	
		turn_over = False
	
		while not self.player_won and not turn_over:
			
			for player in self.players:
				if player.stunned == True:
					player.stunned == False
				else:
					while True:
						player.print_status()
						stance_choice = self.choose_stance()
						player.set_stance(stance_choice)
						
						player_action = self.get_action(player)

						has_attacked = False

						if player_action == 5:
							has_attacked = True

						elif player_action == 4:
							has_attacked = self.map(player, "A")

						elif player_action == 3:
							item_choice = self.select_item(player)
							if item_choice != "e":
								self.use_item(player, item_choice)
							has_attacked = False

						elif player_action == 2:
							ability_choice = self.select_ability(player)

							if ability_choice != 0:
								has_attacked = True
								if ability_choice == 1 or ability_choice == 3:
									target = self.choose_target(player)
									if target == 0:
										has_attacked = False
									else:
										target -= 1
										if player.use_ability(ability_choice, self.enemies[target]):
											self.kills += 1
								else:
									player.use_ability(ability_choice)
							
						elif player_action == 0: # if player flees 
							return True # exit and make flee true

						else:
							target = self.choose_target(player)
							if target == False:
								has_attacked = False
							else:
								target -= 1
								has_attacked = True
								modifier = self.can_see(player, self.enemies[target])[1]

								if player.attack_enemy(self.enemies[target], modifier):
									self.kills += 1
					
						turn_over = True
						if not has_attacked:
							turn_over = False
						else:
							player.adrenaline = player.max_adrenaline
							self.player_won = True
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

		if not self.player_won:
			self.app.write("Enemies' Turn:")
			self.app.write("")
			time.sleep(1)

			for enemy in self.enemies:
				if enemy.health > 0 and not self.player_lost:
					if enemy.stunned == True:
						enemy.stunned = False
					else:
						players = [x for x in self.players]
						for player in players:
							if not self.can_see(enemy, player)[0]:
								players.remove(player)
						if not self.player_lost:
							if len(players) == 0:
								players = self.ai_map(enemy)
							if len(players) != 0:
								player_index = random.randint(0, len(players) - 1)
								player = players[player_index]
								mod = self.can_see(enemy, player)
								loss = enemy.move(player, mod[1])
								self.losses.append(loss)
								if loss == True:
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
											game_over = False
									if game_over:
										self.player_lost = True
										self.app.write("Your party has been killed by your enemies.")
										self.app.write("")
										time.sleep(1)
										self.player_lost = True
										return True
				enemy.adrenaline = enemy.max_adrenaline
