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
import map
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
		self.battle_map = map.make_map(20, 20)
		self.initailised = False
	
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
				return (self.wins, self.kills, True)
			self.do_enemy_actions()
			
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
		player_race =player.__class__.__name__

		while True:
			try:
				self.app.write("Select your ability:")
				if player_race in ["Ethereal","Psionic"] and self.player.adrenaline >= 10:
					self.app.write("	1. Throw (10 ap)")
				if player.adrenaline >= 20:
					self.app.write("	2. Shield (20 ap)")
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
				self.app.write("	1. Medkit ({} ~ available)".format(player.medikits))
				self.app.write("	"+"-"*20)
				if len(player.inventory) > 0:
					for i, item in enumerate(self.player.inventory, 2):
						self.app.write("	{}. {} ({} ~ available)".format(i, item, item.ammount))
				else:
					self.app.write("	No custom items in inventory")
				self.app.write("	"+"-"*20)
				self.app.write("	0. Back")
				self.app.wait_variable(self.app.inputVariable)
				item_choice = self.app.inputVariable.get()

				if item_choice == "quit":
					self.app.quit()

				elif int(item_choice) in [0, 1]:
					return int(item_choice)

				elif int(item_choice) - 2 in range(len(player.inventory)):
					return int(item_choice)

				else:
					raise ValueError


			except ValueError:
				self.app.write("You must enter a valid choice")
				self.app.write("")

	def choose_target(self):
		""" Selects the target of the player's action """
		while True:
			try:
				self.app.write("Choose your target:")
				# use j to give a number option
				j = 0
				while j < len(self.enemies):
					if self.enemies[j].health > 0:
						self.app.write(str(j) + ". " + self.enemies[j].name)
					j += 1
				self.app.write("")
				self.app.wait_variable(self.app.inputVariable)
				target = self.app.inputVariable.get()

				if target == 'quit':
					self.app.quit()

				target = int(target)
				if not (target < len(self.enemies) and target >= 0) or self.enemies[target].health <= 0:
					raise ValueError
				else:
					break
					
			except ValueError:
				self.app.write("You must enter a valid choice")
				self.app.write("")

		return target

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

	def map(self, player):
		if self.initailised == True:
			pass
		else:
			self.generate()
			self.select_spawnpoints()
			self.map(player)

	def generate(self):
		"""generate Method ~
		This method generates a battle map for the
		current battle. The map contains:
		 ~ 3 buildings
		 ~ 16 benches
		 ~ 8 spawn points.
		"""
		self.initailised = True
		benches = []
		buildings = []
		spawnpoints = []
		while len(buildings) <= 3:
			x = random.randint(5, len(self.battle_map)-5)
			y = random.randint(5, len(self.battle_map[0])-5)
			if self.battle_map[x][y] == 0:
				buildings.append((x, y))
				for i in range(x, x + 5):
					for j in range(y, y + 5):
						self.battle_map[i][j] = 2
		del buildings
		while len(benches) <= 16:
			x = random.randint(3, len(self.battle_map)-3)
			y = random.randint(3, len(self.battle_map[0])-3)
			type = random.randint(0, 1)
			if self.battle_map[x][y] == 0:
				benches.append((x, y, type))
				if type == 0:
					for i in range(x, x + 3):
						self.battle_map[i][y] = 1
				else:
					for i in range(y, y + 3):
						self.battle_map[x][i] = 1
		del benches
		while len(spawnpoints) <= 4:
			x = random.randint(3, len(self.battle_map)/4)
			y = random.randint(3, len(self.battle_map[0])/4)
			if self.battle_map[x][y] == 0:
				spawnpoints.append((x, y))
				self.battle_map[x][y] = 3
		while len(spawnpoints) <= 8:
			x = random.randint(3, 3 * len(self.battle_map)/4)
			y = random.randint(3, 3 * len(self.battle_map[0])/4)
			if self.battle_map[x][y] == 0:
				spawnpoints.append((x, y))
				self.battle_map[x][y] = 4
		del spawnpoints
		



	def do_player_actions(self):
		""" Performs the player's actions """
	
		turn_over = False
	
		while not self.player_won and not turn_over:
			
			for player in self.players:
				player.print_status()
				stance_choice = self.choose_stance()
				player.set_stance(stance_choice)
				
				player_action = self.get_action(player)

				has_attacked = False

				if player_action == 5:
					has_attacked = True

				if player_action == 4:
					self.map(player)

				if player_action == 3:
					item_choice = self.select_item(player)
					if item_choice != 0:
						if item_choice == 1:
							has_attacked = player.use_medikit()
						else:
							has_attacked = player.inventory[item_choice - 2].use(player)

				elif player_action == 2:
					ability_choice = self.select_ability(player)

					if ability_choice != 0:
						has_attacked = True
						if ability_choice == 1 or ability_choice == 3:
							target = self.choose_target()
							if player.use_ability(ability_choice, self.enemies[target]):
								self.kills += 1
						else:
							player.use_ability(ability_choice)
					
				if player_action == 0: # if player flees 
					return True # exit and make flee true

				else:
					target = self.choose_target()
					has_attacked = True

					if player.attack_enemy(self.enemies[target]):
						self.kills += 1
			
				turn_over = True
				if not has_attacked:
					turn_over = False
				else:      
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

	def do_enemy_actions(self):
		""" Performs the enemies' actions """

		if not self.player_won:
			self.app.write("Enemies' Turn:")
			self.app.write("")
			time.sleep(1)

			for enemy in self.enemies:
				if enemy.health > 0 and not self.player_lost:

					if not self.player_lost:
						for i in range(0, len(self.players)):
							player = self.players[i]
							loss = enemy.move(player)
							self.losses.append(loss)
							if loss == True:
								index = self.players.index(player)
								self.app.write(
										"{} the {} has perished on the field of battle".format(
											player.name, player.__class__.__name__
										)
									)
								self.app.write("")
								time.sleep(1)
								self.players.pop(index)
								if len(self.players) == 0:
									self.player_lost = True
									self.app.write("Your party has been killed by your enemies.")
									self.app.write("")
									time.sleep(1)
									self.player_lost = True
									return None
